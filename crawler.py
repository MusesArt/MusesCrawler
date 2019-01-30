import requests
from bs4 import BeautifulSoup
import MySQLdb
import random
import os
from faker import Faker
import json

faker = Faker(locale='zh_CN')

# url_pool = {
#     "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.76.342b34e38uhCTQ&id=26076416408&skuId=4009889138236&user_id=1036275215&cat_id=2&is_b=1&rn=ab1de1324ef84c925ebecca404e7036c":
#         '<p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/1036275215/TB2UC84cjnD8KJjSspbXXbbEXXa_!!1036275215.jpg" class="img-ks-lazyload"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/1036275215/TB2WsXBhSCWBuNjy0FhXXb6EVXa_!!1036275215.jpg" class="img-ks-lazyload" data-spm-anchor-id="a220o.1000855.0.i0.50813b53SsihXC"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1036275215/TB2W8fbb0cnBKNjSZR0XXcFqFXa_!!1036275215.jpg" class="img-ks-lazyload"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/1036275215/TB28s2Tb2ImBKNjSZFlXXc43FXa_!!1036275215.jpg" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/1036275215/O1CN01Jg3HXs1oOVyMtfhMe_!!1036275215.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i4/1036275215/O1CN011oOVxQtIWSWCQiB_!!1036275215.jpg" align="absmiddle" class="img-ks-lazyload"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/1036275215/TB21UN4ccLJ8KJjy0FnXXcFDpXa_!!1036275215.jpg" class="img-ks-lazyload"></p>',
#     "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.136.342b34e38uhCTQ&id=566539989730&user_id=880097111&cat_id=2&is_b=1&rn=ab1de1324ef84c925ebecca404e7036c&sku_properties=10142888:21968":
#         '<div class="content ke-post" style="height: auto;"><img class="desc_anchor img-ks-lazyload" id="desc-module-1" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i4/880097111/TB2Ki09xY1YBuNjSszeXXablFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload" data-spm-anchor-id="a220o.1000855.0.i0.6864abd6KYfAtS"><img src="https://img.alicdn.com/imgextra/i1/880097111/TB2faPzx9tYBeNjSspkXXbU8VXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB21KRZf8smBKNjSZFsXXaXSVXa_!!880097111.gif" align="absmiddle" class="img-ks-lazyload"><img class="desc_anchor img-ks-lazyload" id="desc-module-2" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2whddx3mTBuNjy1XbXXaMrVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i4/880097111/TB2qyBWxVOWBuNjy0FiXXXFxVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/880097111/TB2BRkfikZmBKNjSZPiXXXFNVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2FF72pBmWBuNkSndVXXcsApXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img class="desc_anchor img-ks-lazyload" id="desc-module-3" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2dgx8x79WBuNjSspeXXaz5VXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i4/880097111/TB2F8m.irsrBKNjSZFpXXcXhFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/880097111/TB2N53nx_JYBeNjy1zeXXahzVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2Di.nx_JYBeNjy1zeXXahzVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img class="desc_anchor img-ks-lazyload" id="desc-module-4" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i3/880097111/TB20nOFxYSYBuNjSspfXXcZCpXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/880097111/TB20uoTpByWBuNkSmFPXXXguVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2NFFkpTXYBeNkHFrdXXciuVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2jMukisj_B1NjSZFHXXaDWpXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i4/880097111/TB26tqcx1uSBuNjy1XcXXcYjFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img class="desc_anchor img-ks-lazyload" id="desc-module-5" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2r4pvx29TBuNjy0FcXXbeiFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/880097111/TB2p85ex1uSBuNjSsziXXbq8pXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2ofGkx7OWBuNjSsppXXXPgpXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/880097111/TB2dkFtx4SYBuNjSsphXXbGvVXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img class="desc_anchor img-ks-lazyload" id="desc-module-6" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><img src="https://img.alicdn.com/imgextra/i2/880097111/TB2hAG1x7SWBuNjSszdXXbeSpXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/880097111/TB2KO7.pyOYBuNjSsD4XXbSkFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/880097111/TB2BRBRblcXBuNjt_biXXXpmpXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i4/880097111/TB2ZmmNvH5YBuNjSspoXXbeNFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/880097111/TB2HjNWblgXBuNjt_hNXXaEiFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/880097111/TB2ZC5DvH1YBuNjSszeXXablFXa_!!880097111.jpg" align="absmiddle" class="img-ks-lazyload"> </p></div>',
#     "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.196.342b34e38uhCTQ&id=566379682565&user_id=2068607660&cat_id=2&is_b=1&rn=ab1de1324ef84c925ebecca404e7036c":
#         '<div class="content ke-post" style="height: auto;"><img class="desc_anchor img-ks-lazyload" id="desc-module-1" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/2068607660/TB2uex2fmCWBuNjy0FhXXb6EVXa_!!2068607660.jpg" class="img-ks-lazyload"></p><img class="desc_anchor img-ks-lazyload" id="desc-module-2" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p>&nbsp;</p><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i4/2068607660/TB2j5YcfoR1BeNjy0FmXXb0wVXa_!!2068607660.jpg" class="img-ks-lazyload"></p><p>&nbsp;</p><img class="desc_anchor img-ks-lazyload" id="desc-module-3" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/2068607660/TB2JnqpfhSYBuNjSspjXXX73VXa_!!2068607660.jpg" class="img-ks-lazyload"></p><img class="desc_anchor img-ks-lazyload" id="desc-module-4" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i1/2068607660/TB2Pl8WfbGYBuNjy0FoXXciBFXa_!!2068607660.jpg" class="img-ks-lazyload"></p><img class="desc_anchor img-ks-lazyload" id="desc-module-5" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/2068607660/TB2BT8PfXmWBuNjSspdXXbugXXa_!!2068607660.jpg" class="img-ks-lazyload"></p><img class="desc_anchor img-ks-lazyload" id="desc-module-6" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><img align="absmiddle" src="https://img.alicdn.com/imgextra/i3/2068607660/TB2HkamfeuSBuNjy1XcXXcYjFXa_!!2068607660.jpg" class="img-ks-lazyload" data-spm-anchor-id="a220o.1000855.0.i0.2ae5452ezS24EZ"><img align="absmiddle" src="https://img.alicdn.com/imgextra/i2/2068607660/TB2LhR3fXuWBuNjSszbXXcS7FXa_!!2068607660.jpg" class="img-ks-lazyload"></p><p>&nbsp;</p></div>',
#     "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.281.342b34e38uhCTQ&id=20077357535&skuId=91171224020&user_id=1665565454&cat_id=2&is_b=1&rn=ab1de1324ef84c925ebecca404e7036c":
#         '<div class="content ke-post" style="height: auto;"><img class="desc_anchor img-ks-lazyload" id="desc-module-1" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i4/1665565454/TB2L.S3fXmWBuNjSspdXXbugXXa_!!1665565454.jpg" alt="PC-790_01.jpg" class="img-ks-lazyload" data-spm-anchor-id="a220o.1000855.0.i0.695a5a63HzdeiV"><br> <img src="https://img.alicdn.com/imgextra/i3/1665565454/TB2wDvJfkCWBuNjy0FaXXXUlXXa_!!1665565454.jpg" alt="PC-790_02.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i1/1665565454/TB2vUvwfeOSBuNjy0FdXXbDnVXa_!!1665565454.jpg" alt="PC-790_03.jpg" class="img-ks-lazyload"><br><img class="desc_anchor img-ks-lazyload" id="desc-module-2" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i1/1665565454/TB2DiLDfhSYBuNjSspjXXX73VXa_!!1665565454.jpg" alt="PC-790_04.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i1/1665565454/TB25P2Mfb9YBuNjy0FgXXcxcXXa_!!1665565454.jpg" alt="PC-790_05.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i1/1665565454/TB2bEPwfeOSBuNjy0FdXXbDnVXa_!!1665565454.jpg" alt="PC-790_07.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i4/1665565454/TB2oj50fgmTBuNjy1XbXXaMrVXa_!!1665565454.jpg" alt="PC-790_08.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i3/1665565454/TB215EpfoR1BeNjy0FmXXb0wVXa_!!1665565454.jpg" alt="PC-790_09.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i4/1665565454/TB2ezzhfb1YBuNjSszeXXablFXa_!!1665565454.jpg" alt="PC-790_10.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i2/1665565454/TB2_R_Mfh9YBuNjy0FfXXXIsVXa_!!1665565454.jpg" alt="PC-790_11.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i2/1665565454/TB2tuLifkOWBuNjSsppXXXPgpXa_!!1665565454.jpg" alt="PC-790_12.jpg" class="img-ks-lazyload"><br><img class="desc_anchor img-ks-lazyload" id="desc-module-3" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i2/1665565454/TB26W.KfnlYBeNjSszcXXbwhFXa_!!1665565454.jpg" alt="PC-790_13.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i1/1665565454/TB2qXLmff5TBuNjSspcXXbnGFXa_!!1665565454.jpg" alt="PC-790_14.jpg" class="img-ks-lazyload"><br><img class="desc_anchor img-ks-lazyload" id="desc-module-4" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i1/1665565454/TB2WMHxfh1YBuNjy1zcXXbNcXXa_!!1665565454.jpg" alt="PC-790_15.jpg" class="img-ks-lazyload"><img class="desc_anchor img-ks-lazyload" id="desc-module-5" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><img src="https://img.alicdn.com/imgextra/i2/1665565454/TB2MzkpfoR1BeNjy0FmXXb0wVXa_!!1665565454.jpg" alt="PC-790_16.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i2/1665565454/TB2lCoUfmBYBeNjy0FeXXbnmFXa_!!1665565454.jpg" alt="PC-790_17.jpg" class="img-ks-lazyload"><br> <img src="https://img.alicdn.com/imgextra/i2/1665565454/TB2XTrqff9TBuNjy1zbXXXpepXa_!!1665565454.jpg" alt="PC-790_18.jpg" class="img-ks-lazyload"><br><img class="desc_anchor img-ks-lazyload" id="desc-module-6" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><span style="color: #ffffff;font-size: 12.0px;">------------</span><br></p><img class="desc_anchor img-ks-lazyload" id="desc-module-7" src="https://assets.alicdn.com/kissy/1.0.0/build/imglazyload/spaceball.gif"><p><span style="color: #ffffff;font-size: 12.0px;">------------</span><br></p></div>',
#     "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.71.342b34e32AHdYK&id=534819372196&skuId=3216528110746&user_id=1639091771&cat_id=2&is_b=1&rn=ab1de1324ef84c925ebecca404e7036c":
#         '<p><img src="//gdp.alicdn.com/imgextra/i4/1639091771/T2tg_IXc8aXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i1/1639091771/T20PGDXeFcXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i1/1639091771/T2ZsYkXiVbXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i4/1639091771/T29a2JXeFXXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i1/1639091771/T2cE_IXeXXXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i2/1639091771/T2xsyHXeNbXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i4/1639091771/T2VgknXehaXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i3/1639091771/T26AQnXhdaXXXXXXXX_!!1639091771.jpg" alt="" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i2/1639091771/T2qI_CXmhaXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"> <img src="//gdp.alicdn.com/imgextra/i3/1639091771/T2a_TbXfVbXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i2/1639091771/T27QquXn8bXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"><img src="//gdp.alicdn.com/imgextra/i4/1639091771/T2ugslXbXaXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload" data-spm-anchor-id="a220o.1000855.5003-14434150737.i0.162d1966ola9CW"><img src="//gdp.alicdn.com/imgextra/i3/1639091771/TB2k4UqdpXXXXa3XXXXXXXXXXXX_!!1639091771.jpg" align="absmiddle" class="img-ks-lazyload"></p>',
#     "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.26.342b34e32AHdYK&id=41656615863&user_id=752144854&cat_id=2&is_b=1&rn=ab1de1324ef84c925ebecca404e7036c&sku_properties=10142888:21968":
#         '<p><img src="https://img.alicdn.com/imgextra/i1/752144854/TB2X9yXdUhnpuFjSZFpXXcpuXXa-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/752144854/TB2IFiflFXXXXXDXpXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/752144854/TB2jMJZlFXXXXcfXXXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload" data-spm-anchor-id="a220o.1000855.0.i0.34e74b15fDRLWP"><img src="https://img.alicdn.com/imgextra/i4/752144854/TB2ZVmrlFXXXXbIXXXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/752144854/TB2r78_lFXXXXauXpXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/752144854/TB2k.utlFXXXXbeXXXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/752144854/TB2oV4YlFXXXXa9XpXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/752144854/TB2DL.cipXXXXaAXpXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/752144854/TB2FXKylFXXXXavXXXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i4/752144854/TB2yGeplFXXXXbPXXXXXXXXXXXX-752144854.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/752144854/TB2teD.mrFlpuFjy0FgXXbRBVXa-752144854.jpg" align="absmiddle" class="img-ks-lazyload"></p>'
# }

url_pool = {
    "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.96.1dde34e3XLWAB2&id=562465104224&areaId=330100&user_id=1776918235&cat_id=2&is_b=1&rn=ac39776227c47fd6458c89542a8de4d9&sku_properties=10142888:94464574":
        '<p><img src="https://img.alicdn.com/imgextra/i1/1776918235/O1CN012Ahg4Mxsqnxp8TM_!!1776918235.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/1776918235/O1CN012Ahg4Mxr2XqrqrE_!!1776918235.jpg" align="absmiddle" class="img-ks-lazyload" data-spm-anchor-id="a220o.1000855.0.i0.23067b99JECQf1"><img src="https://img.alicdn.com/imgextra/i3/1776918235/O1CN012Ahg4Mi5NXLJF12_!!1776918235.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i2/1776918235/O1CN012Ahg4NHu7cvxt9n_!!1776918235.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i3/1776918235/O1CN012Ahg4OMXFz0ITng_!!1776918235.jpg" align="absmiddle" class="img-ks-lazyload"><img src="https://img.alicdn.com/imgextra/i1/1776918235/O1CN012Ahg4LcJDGElkZg_!!1776918235.jpg" align="absmiddle" class="img-ks-lazyload"></p>'
}

db = MySQLdb.connect("localhost", "root", "123456", "musesart", charset='utf8')
cursor = db.cursor()



for url, description in url_pool.items():
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text,"html.parser")

    print("商品名称")
    name = soup.find('div', {'class': "tb-detail-hd"}).h1.get_text().strip()
    # title = title.replace("Nike","").replace("耐克官方","").strip()
    print(name)

    print("商品简介")
    brief = soup.find('div', {'class': "tb-detail-hd"}).p.get_text().strip()
    print(brief)

    print("商品价格")
    price = [random.randint(200,500)//10*10+8, random.randint(200,500)//10*10+8-random.randint(0,5)*10]
    print(price)

    print("商品主图")
    images = soup.find(id="J_UlThumb").findAll("img")
    image_list = []
    for image in images:
        src = image.get("src")
        pos = src.rfind("_")
        src = src[:pos]
        image_list.append("https:"+src)
    print(image_list)

    attr_without_image = soup.find('div',{'class':"tb-sku"}).find('dt').get_text()
    print(attr_without_image)
    values_without_image_list = []
    values_without_image = soup.find('div',{'class':"tb-sku"}).find('ul').findAll('li')
    for value in values_without_image:
        values_without_image_list.append(value.find('span').get_text())
    print(values_without_image_list)

    attr_with_image = soup.find('div',{'class':"tb-sku"}).find('dl',{"class":"tm-img-prop"}).find('dt').get_text()
    print(attr_with_image)

    dic = {}
    values_with_image = soup.find('div',{'class':"tb-sku"}).findAll('li')
    for value in values_with_image:
        temp = value.find('a').get("style")
        key = value.find('span').get_text()
        if temp!=None:
            url = temp.split("url(")[1].split(") center")[0]
            pos = url.rfind("_")
            url = url[:pos]
            dic[key] = "https:"+url
    print(dic)

    information = {}
    infos = soup.find('div',{'class':'attributes-list'}).find('ul').findAll("li")
    for info in infos:
        temp = info.get_text().split(": ")
        information[temp[0]] =  "".join(temp[1].split())
    information = json.dumps(information, ensure_ascii=False)
    print(information)


    """ 插入commodity表 """
    sql = "INSERT INTO commodity (add_time, brief, click_num, cover_image, discount_price, " \
          "goods_num, information, is_hot, `name`, original_price, ship_free, sold_num, update_time, description ) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    faker_time = faker.date_between(start_date='-30d')
    cursor.execute(sql, [faker_time, brief, random.randint(100,500), image_list[0], price[0],
                         random.randint(20,1000), information, 0, name, price[1], 1, random.randint(20,200), faker_time, description.replace("\"","'")])
    db.commit()
    """ 获取商品id """
    sql = "SELECT LAST_INSERT_ID()"
    cursor.execute(sql)
    commodity_id = cursor.fetchone()[0]
    print(commodity_id)

    """ 查询无图属性信息 """
    sql = "INSERT INTO attribute (commodity_id, image_flag, `name`) VALUES (%s, %s, %s)"
    cursor.execute(sql,[commodity_id, 0, attr_without_image])
    db.commit()
    sql = "SELECT LAST_INSERT_ID()"
    cursor.execute(sql)
    attribute_id = cursor.fetchone()[0]

    """ 插入parameter表 无图属性 """
    for value in values_without_image_list:
        sql = "INSERT INTO parameter (attribute_id, `value`) VALUES(%s, %s)"
        cursor.execute(sql, [attribute_id, value])
    db.commit()

    """ 查询有图属性信息 """
    sql = "INSERT INTO attribute (commodity_id, image_flag, `name`) VALUES (%s, %s, %s)"
    cursor.execute(sql, [commodity_id, 1, attr_with_image])
    db.commit()
    sql = "SELECT LAST_INSERT_ID()"
    cursor.execute(sql)
    attribute_id = cursor.fetchone()[0]

    """ 插入parameter表 有图属性 """
    for value, image in dic.items():
        sql = "INSERT INTO parameter (attribute_id, image, `value`) VALUES(%s,%s,%s)"
        cursor.execute(sql, [attribute_id, image, value])
    db.commit()

    """ 插入image表 商品主图 """
    for image in image_list:
        sql = "INSERT INTO image (image_url, commodity_id) VALUES(%s, %s)"
        cursor.execute(sql, [image, commodity_id])
    db.commit()




