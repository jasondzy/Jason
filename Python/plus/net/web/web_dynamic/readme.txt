
#########################

# Note:这里是把web_service这个python程序当做了主体，通过在web_service程序中
       来调用web框架
#这里使用的是wsgi的网关接口协议，主要的就是在服务器函数中调用application(
 environ,start_repose)函数,在framework脚本中实现这个application函数。而start_respose正好反过来，service中实现，frame中调用


#########################