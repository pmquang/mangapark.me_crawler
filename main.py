#!/usr/bin/python
# -*- coding: utf-8 -*-
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, GetPost
from wordpress_xmlrpc.methods.users import GetUserInfo

wp = Client('http://emanga24h.info/xmlrpc.php','quangpm3','xxxxxx')
#tmp = wp.call(GetPost(49))
#print wp.call(GetUserInfo())



post = WordPressPost()
post.title = u'Test thumnail hình ảnh'
post.content = u'''Test thumnail hình ảnh'''
post.terms_names = { 
    'post_tag': ['test', 'firstpost'],
    'category': ['Puppet']
}
#post.thumbnail = 'http://s3.amazonaws.com/static.graphemica.com/glyphs/i500s/000/010/380/original/0110-500x500.png'
post.post_status = 'publish'
wp.call(NewPost(post))
