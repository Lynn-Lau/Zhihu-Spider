## Zhihu-Spider 知乎爬虫

使用语言为Python 2.7.10，配合使用的框架为Scrapy，可以运行在Linux/Windows/Mac OS系统。在整个工程中zhuhu1_spider.py 文件中最重要的函数为登录函数，下面对登录函数进行解释：

```python
# 此函数为登录函数
def post_login(self,response):
        print 'Preparing login'

        # 在返回的html代码中抓取xsrf验证机制字段，并进行打印
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()
        print xsrf

        # FormRequest.from_response()函数是scrapy框架自带的函数，用于请求登录表单
        # 请求登录表单后将需要填写的内容填写之后，调用after_login函数
        return [
            FormRequest.from_response(response,
                                      # meta 函数是对cookie获取，用于被跟踪
                                      meta = {'cookiejar' : response.meta['cookiejar']},
                                      # headers 伪装
                                      headers = self.headers,
                                      # 将验证机制，email,password 填写进去
                                      formdata = {
                                          'xsrf' : xsrf,
                                          'email' : 'Your E-mail',
                                          'passsword' : 'Your Password',
                                      },
                                      # 调用after_login函数
                                      callback = self.after_login,

                                      dont_filter = True
                                      )
        ]
```

上面函数正常运行之后，通过工程中的pipelines等文件中函数对运行结果进一步处理可以得到一下输出，整个输出均存储在.json的文件中
文件内容示例如下：

<pre><code>
{"name": ["xxx"], "business": ["高等教育"], "url": "http://www.zhihu.com/people/xxx", "AskAnswerPostLog": [], "thanks": ["46984"], "education": [], "agree": ["247347"]}
{"name": ["xxx"], "business": [], "url": "http://www.zhihu.com/people/zxxx", "AskAnswerPostLog": [], "thanks": ["2009"], "education": [], "agree": ["4244"]}
{"name": ["xxx"], "business": [], "url": "http://www.zhihu.com/people/xxxxxx", "AskAnswerPostLog": [], "thanks": ["2206"], "education": [], "agree": ["9412"]}
{"name": ["xxx"], "business": [], "url": "http://www.zhihu.com/people/xxxxx", "AskAnswerPostLog": [], "thanks": ["29222"], "education": [], "agree": ["94618"]}
{"name": ["xxx"], "business": ["互联网"], "url": "http://www.zhihu.com/people/xxxx", "AskAnswerPostLog": [], "thanks": ["4778"], "education": [], "agree": ["13459"]}
{"name": ["xxx"], "business": [], "url": "http://www.zhihu.com/people/xxxxx", "AskAnswerPostLog": [], "thanks": ["52172"], "education": [], "agree": ["193739"]}
{"name": ["xxx"], "business": ["培训"], "url": "http://www.zhihu.com/people/xxxxx", "AskAnswerPostLog": [], "thanks": ["2869"], "education": ["北京航空航天大学"], "agree": ["16651"]}
{"name": ["xxx"], "business": [], "url": "http://www.zhihu.com/people/xxxxxxx", "AskAnswerPostLog": [], "thanks": ["265773"], "education": [], "agree": ["1442074"]}
</pre></code>
