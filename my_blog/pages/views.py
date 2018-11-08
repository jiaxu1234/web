#coding:utf-8
from django.shortcuts import render

def display(request):
    return render(request, 'love.html', )

def bookmarks(request):
    return render(request, 'bookmarks.html' )

def qq(request):
    return render(request, 'qq.html' )

def test(request):
    return render(request, 'test.html' )
