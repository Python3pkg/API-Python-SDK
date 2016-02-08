#/usr/bin/python
import urllib
import httplib2
import requests
import json
import sys
import threading
import signal

class trackvia:
	"""Class that wraps the TrackVia API. This client handles the initial Oauth authentication as well as refreshing the token before expiration."""

	def __init__(self, url, username, password, apikey):
		"""This is a constructor for the TrackVia client."""

		#Register a method to handle signals and close our threads cleanly. Only if part of main thread
		if __name__ == "__main__":
			signal.signal(signal.SIGINT, self.__signal_handler)

		self.base_url=url
		self.apikey=apikey

		#Login information
		values = { 'grant_type' : 'password',
				'client_id' : 'TrackViaAPI',
				'username' : username,
				'password' : password}

		#Actually do the login and parse the token from the response.
		resp,body=self.__json_request("{0}/oauth/token".format(self.base_url),post=values)

		self.token=body['value']
		self.refreshToken=body['refreshToken']
		self.expiresIn=body['expires_in']

		#Get the account ID that we are dealing with here
		get_values= {'access_token' : self.token}
		resp,body=self.__json_request("{0}/users".format(self.base_url), type="GET", get=get_values)
		self.account_id=body['accounts'][0]['id']

		#Schedule a oauth_token refresh 15s before it expires
		self.thread=threading.Timer(self.expiresIn-15, self.__refresh_token)
		self.thread.daemon = True
		self.thread.start()

	# This is a helper class to make requests to the trackvia API
	def __json_request(self,url,type="POST",post=None,get=None,content_type="urlencode"):
		"""This method is used internally for sending requests to the API."""
		if post == None:
			post_data=None
		else:
			try:
				post_data = urllib.urlencode(post)
			except:
				post_data=post

		#Convert get params to be used in the URL
		if get == None:
			get_data=""
		else:
			get_list=[]
			for element in get.keys():
				get_list.append(urllib.quote_plus(element)+"="+urllib.quote_plus(str(get[element])))
			get_data="?"+'&'.join(get_list)

		if content_type=="json":
			headers={'Content-Type': 'application/json; charset=UTF-8'}
		else:
			headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

		h = httplib2.Http()
		response, content = h.request(url+get_data,type,headers=headers,body=post_data)

		try:
			body=json.loads(content)
		except ValueError as e:
			body=content

		return response,body

	# It is much cleaner to upload multipart files using the Requests framework.
	def __post_file(self, url, data, file):
		r = requests.post(url,params=data,files=file)
		return r.status_code, r.content

	def __refresh_token(self):
		"""This method is used internally to refresh the oauth token."""
		#Login information
		values = { 'grant_type' : 'refresh_token',
				'client_id' : 'TrackViaAPI',
				'refresh_token' : self.refreshToken['value']}

		#Actually do the login and parse the token from the response.
		resp,body=self.__json_request("{0}/oauth/token".format(self.base_url),type="POST",post=values)
		self.token=body['value']
		self.refreshToken=body['refreshToken']
		self.expiresIn=body['expires_in']

		self.thread=threading.Timer(self.expiresIn-15, self.__refresh_token)
		self.thread.daemon = True
		self.thread.start()

	def get_all_apps(self):
		"""Returns all apps for the logged in account."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey}
		resp,body=self.__json_request("{0}/openapi/apps".format(self.base_url),type='GET', get=get_values)
		return resp,body

	def get_all_views(self):
		"""Returns all views for the logged in account."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey}
		resp,body=self.__json_request("{0}/openapi/views".format(self.base_url),type='GET', get=get_values)
		return resp,body

	def get_view(self,viewId):
		"""Returns a specific view by the viewId."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId }
		resp,body=self.__json_request("{0}/openapi/views/{1}".format(self.base_url,viewId),type='GET', get=get_values)
		return resp,body

	def find_records(self,viewId,query,start=0,max=50):
		"""Search for records in a view."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"q" : query,
				"start": start,
				"max": max }
		resp,body=self.__json_request("{0}/openapi/views/{1}/find".format(self.base_url, viewId),type='GET', get=get_values)
		return resp,body

	def get_all_records(self,viewId,start=0,max=50):
		"""Returns all records within a view, from start to max."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"q" : "",
				"start": start,
				"max":  max }
		resp,body=self.__json_request("{0}/openapi/views/{1}/find".format(self.base_url, viewId),type='GET', get=get_values)
		return resp,body

	def get_record(self,viewId,recordId):
		"""Returns a specific record from a view."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"recordId" : recordId }
		resp,body=self.__json_request("{0}/openapi/views/{1}/records/{2}".format(self.base_url, viewId, recordId),type='GET', get=get_values)

		return resp,body

	def delete_record(self,viewId,recordId):
		"""Deletes a record in a view."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"recordId" : recordId }
		resp,body=self.__json_request("{0}/openapi/views/{1}/records/{2}".format(self.base_url, viewId, recordId),type='DELETE', get=get_values)
		return resp,body

	def delete_file(self, viewId, recordId, fieldName):
		"""Deletes a file from a field in a view."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"recordId" : recordId }
		resp,body=self.__json_request("{0}/openapi/views/{1}/records/{2}/files/{3}".format(self.base_url, viewId, recordId, fieldName),type='DELETE', get=get_values)
		return resp,body

	def get_file(self, viewId, recordId, fieldName):
		"""Returns a file from a field in a view."""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"recordId" : recordId }
		resp,body=self.__json_request("{0}/openapi/views/{1}/records/{2}/files/{3}".format(self.base_url, viewId, recordId, fieldName),type='GET', get=get_values)
		return resp,body

	def attach_file(self, viewId, recordId, fieldName, file):
		"""Attaches a file to a record"""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"recordId" : recordId }
		file={'file':open(file,'r')}
		resp,body=self.__post_file("{0}/openapi/views/{1}/records/{2}/files/{3}".format(self.base_url, viewId, recordId, fieldName),get_values,file)
		return resp,body

	def create_record(self, viewId, data):
		"""Creates a record in a view"""
		post_data={"data":data}
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId }
		resp,body=self.__json_request("{0}/openapi/views/{1}/records".format(self.base_url, viewId),type='POST', post=json.dumps(post_data), get=get_values, content_type="json")

		return resp,body

	def update_record(self, viewId,  recordId, data):
		"""Updates a record in a view"""
		post_data={"data":data}
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId }
		resp,body=self.__json_request("{0}/openapi/views/{1}/records/{2}".format(self.base_url, viewId, recordId),type='PUT', post=json.dumps(post_data), get=get_values, content_type="json")

		return resp,body

	def delete_record(self, viewId, recordId):
		"""Deletes a record from a view"""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"viewId" : viewId,
				"recordId" : recordId }
		resp,body=self.__json_request("{0}/openapi/views/{1}/records/{2}".format(self.base_url, viewId, recordId),type="DELETE",get=get_values)
		return resp,body

	def get_users(self,start=0,max=50):
		"""Gets users in the account"""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"start" : start,
				"max" : max }
		resp,body=self.__json_request("{0}/openapi/users".format(self.base_url),type="GET",get=get_values)
		return resp,body

	def create_user(self,email,firstName,lastName,timeZone):
		"""Creates a user"""
		get_values={"access_token" : self.token,
				"user_key" : self.apikey,
				"email" : email,
				"firstName" : firstName,
				"lastName" : lastName,
				"timeZone" : timeZone }
		resp,body=self.__json_request("{0}/openapi/users".format(self.base_url),type="POST",get=get_values)
		return resp,body

	def __signal_handler(self, signal, frame):
		"""Internal method for handling signals."""
		print("Caught Signal: {0}".format(signal) )
		self.stop()
		sys.exit(0)

	def stop(self):
		"""Cleanly stop the client and kill the oauth token refresh thread."""
		print("Stopping client")
		self.thread.cancel()
