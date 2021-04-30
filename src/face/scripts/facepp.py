#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pprint import pformat
# import PythonSDK
from PythonSDK.facepp import API, File
# 导入图片处理类
import PythonSDK.ImagePro
import rospy
from face.srv import detect, detectResponse, search, searchResponse, compare, compareResponse


# 此方法专用来打印api返回的信息
def print_result(hit, result):
    print(hit)
    print('\n'.join("  " + i for i in pformat(result, width=75).split('\n')))


def printFuctionTitle(title):
    return "\n" + "-" * 60 + title + "-" * 60


def FaceDetect(request):
    result = api.detect(image_file=File(request.imgPath),
                        return_attributes="age")
    faceVector = [[-1 for j in range(5)] for i in range(3)]
    # AddFace(result["faces"])#将face加入faceSet
    for num, face in enumerate(result['faces']):
        faceVector[num][0] = int(face['face_rectangle']['top'])
        faceVector[num][1] = int(face['face_rectangle']['left'])
        faceVector[num][2] = int(face['face_rectangle']['width'])
        faceVector[num][3] = int(face['face_rectangle']['height'])
        faceVector[num][4] = int(face['attributes']['age']['value'])
        detectResponse(result['face_num'], *faceVector)
    # print_result(printFuctionTitle("人脸检测"), res)
    return detectResponse(int(result['face_num']), *faceVector)


def FaceCompare(request):
    result = api.compare(image_file1=File(request.srcPath),
                         image_file2=File(request.dstPath))
    # print_result(printFuctionTitle("人脸对比"), result)
    return compareResponse(int(result['confidence']))


def FaceSearch(request):
    return searchResponse("ok")


# result = api.search(image_file=File(request.face_search_img), outer_id='faceSet')
# print_result(printFuctionTitle("人脸查找"), result)


def AddFace(faceList):
    faceResStr = ""
    for index in range(len(faceList)):
        if index == 0:
            faceResStr = faceResStr + faceList[index]["face_token"]
        else:
            faceResStr = faceResStr + "," + faceList[index]["face_token"]
    api.faceset.addface(outer_id='faceSet', face_tokens=faceResStr)


if __name__ == '__main__':
    api = API()  # 初始化API
    print(__version__)
    # api.faceset.delete(outer_id='faceSet', check_empty=0)#删除faceSet
    # ret = api.faceset.create(outer_id='faceSet')#创建一个新的faceSet
    rospy.init_node('face')  # ROS节点初始化
    detectServer = rospy.Service('/face_detect', detect,
                                 FaceDetect)  # 注册人脸识别服务和相应的回调函数
    compareServer = rospy.Service('/face_compare', compare,
                                  FaceCompare)  # 注册人脸对比服务和相应的回调函数
    searchServer = rospy.Service('/face_search', search,
                                 FaceSearch)  # 注册人脸对比服务和相应的回调函数
    rospy.loginfo("Service ready")
    rospy.spin()
