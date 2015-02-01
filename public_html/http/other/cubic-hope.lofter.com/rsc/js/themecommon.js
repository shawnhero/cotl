(function(){
	var loadJquery = function(_callback) {
		var _url = "http://l.bst.126.net/rsc/js/jquery-1.6.2.min.js";
		var _script = document.createElement('script');
		_script.type = 'text/javascript';
		(navigator.appVersion.indexOf("MSIE") != -1) ? _script.onreadystatechange = _callback
				: _script.onload = _callback;
		if (_url != '') {
			_script.src = _url;
		}
		document.getElementsByTagName('head')[0].appendChild(_script);
	};

	var commonFunc = function() {
		if (!!window.Theme&&!!window.Theme.ImageProtected) {
			$(document).delegate('img', 'contextmenu', function(event){
				if (/^http:\/\/img(lf\d*|size|\d*)\.ph\.126\.net\/.+$/.test($(this).attr('src'))) {
					 $("#context_content").remove();
		             $("<div id='context_content' oncontextmenu='return false;' style='z-index:99999;color:#fff;position:absolute;background:#000;padding:8px;opacity:.8;filter:alpha(opacity=80);border-radius:3px;'>" + window.Theme.ContextValue + "</div>").appendTo("body")
		                .css("left", event.pageX)
		                .css("top", event.pageY)
		                .show().delay(3000).fadeOut('fast');
					event.returnValue=false;
					return false;
				}
			});
			$(document).click(function(event){
				$("#context_content").remove();
			});
			$('img').click(function(event){
				$("#context_content").remove();
			});
		}

		if (!!window.pagewidget) {
			$('input').bind('keydown', function(event){
				event.stopPropagation();
		        return true;
			});
			$(document).bind('keydown', function(event){
				if (!!window['__photo_showing_lock__']) {
					return true;
				}
				if (event.keyCode == 75 || event.keyCode == 39) {
					var nextLink = $('#__next_permalink__').attr('href');
					if (!!nextLink) {
						location.href = nextLink;
					}
					return false;
				}
				if (event.keyCode == 74 || event.keyCode == 37) {
					var prevLink = $('#__prev_permalink__').attr('href');
					if (!!prevLink) {
						location.href = prevLink;
					}
					return false;
				}
			});
		}
		
		//LOFTER-16520:LOFTER个人主页注册引导功能 (弹层逻辑)
		initLofterRegLoginLayer();
	};

	try {
		if(!window.jQuery) {
		   loadJquery(commonFunc);
		} else {
			$(document).ready(commonFunc);
		}
	} catch(e) {

	}
	
	//LOFTER-16520:LOFTER个人主页注册引导功能 (弹层逻辑)
	function initLofterRegLoginLayer(){
		var __cookieKey1 = 'reglogin_doopen';
		var __cookieKey2 = 'reglogin_hasopened';
		var __cookieKey_loginFlag = 'reglogin_isLoginFlag';
		var __isLogin = true;
		
		//cookie相关
		var __cookies,                      // cookie数据缓存
	    __resp = /\s*\;\s*/,            // cookie分隔符
	    __date = new Date(),            // cookie涉及的时间处理对象
	    __currentms = __date.getTime(), // 当前时间值
	    __milliseconds = 24*60*60*1000; // 一天的毫秒数值
		
		var __getCookieStr = function(_key,_value){
		    if (arguments[3])
		        __date.setTime(__currentms+arguments[3]*__milliseconds);
		    var _path = arguments[4]?('path='+arguments[4]+';'):'',
		        _domain = arguments[2]?('domain='+arguments[2]+';'):'',
		        _expires = arguments[3]?('expires='+__date.toGMTString()+';'):'';
		    return _key+'='+_value+';'+_domain+_path+_expires;
		};
		
		var getCookie = function(_key){
		    return __cookies[_key]||'';
		};
		
		var delCookie = function(_key){
		    document.cookie = __getCookieStr(_key,'',arguments[1],-100,arguments[2]);
		    delete __cookies[_key];
		};
		
		var setCookie = function(_key,_value){
		    document.cookie = __getCookieStr.apply(null,arguments);
		    __cookies[_key] = _value;
		};
		
		var refreshCookie = function(){
		    __cookies = {};
		    for(var i=0,_arr=document.cookie.split(__resp),l=_arr.length,_index;i<l;i++){
		        _index = _arr[i].indexOf('=');
		        __cookies[_arr[i].substring(0,_index)] = _arr[i].substr(_index+1);
		    }
		};
		
		refreshCookie();
		
		//事件相关
		var stopBubble = function(_event) {
			_event = _event ? _event : window.event;
			if(!_event) return;
			if(!!(window.attachEvent &&!window.opera)) {
				_event.cancelBubble = true;
			} else {
				_event.stopPropagation();
			}
			return _event;
		};
		
		var stopDefault = function(_event){
			_event = _event ? _event : window.event;
			if (!_event) return;
		    !!_event.preventDefault
		    ? _event.preventDefault()
		    : _event.returnValue = false;
		};
		
		var stopEvent = function(_event){
			stopBubble(_event);
			stopDefault(_event);
		};
		
		var showRegLoginLayer = function(){
			var _loginFlag = getCookie(__cookieKey_loginFlag);
			if(__isLogin && _loginFlag=='1') return;
			
			var _options = {
					'class' : 'w-pagelayer-reglogin',
					'html' : '',
					'isNeedAnimation' : true,
					'opacity' : 80,
					'bgcolor' : '#000',
					'zIndex' : 2000,
					'showClosedIcon' : true,
					'noDocClickDestroy'  :true,
					'notSetContMinHeight' : true,
					'cbAfterSetHtmlContent' : function(_lycont) {
						if(!!_lycont && !!_lycont.parentNode && !!_lycont.parentNode.parentNode && !!_lycont.parentNode.parentNode.parentNode){
							var _pagelayer = _lycont.parentNode.parentNode.parentNode;
							var _lyHeight = _pagelayer.clientHeight || 1;
							if(_lyHeight>450){
								_lycont.style.paddingTop = Math.floor((_lyHeight-450)/2) + 'px';
							} else{
								_lycont.style.paddingTop = 0;
							}
						}
					}._$bind(this)
			};
			
			_options.html = '<div class="m-reglogin">\
				                 <div style="display:none" class="logo">\
				                     <h1 class="f1">LOFTER</h1>\
				                     <h2 class="f2">快速<span class="f3">、</span>漂亮<span class="f3">、</span>有趣的记录方式</h2>\
				                 </div>\
				                 <div class="iframewrap">\
				                     <iframe width="1080" height="670" frameborder="0" border="0" scrolling="no" marginheight="0" marginwidth="0" allowtransparency="true" src="http://www.lofter.com/loginiframe?from=personalPage&target='+location.href+'"></iframe>\
				                 </div>\
				             </div>';
			
			
			var pageLayer = netease.lofter.widget.pageLayer._$getInstance(document.body, _options);
			
		};
		
		window.showRegLoginLayer = showRegLoginLayer;//接口全局化
		
		//LOFTER-16834:在非登陆状态下，用户在个人主页模板页面，第一次进入不弹出注册层，第二次弹出注册层，只弹出一次
		var _dealOpenLogic = function dealOpenLogic(){
			if(dealOpenLogic.isExeced) return;
			dealOpenLogic.isExeced = true;
			if(!__isLogin){
				var _doOpened = getCookie(__cookieKey1);
				var _hasOpened = getCookie(__cookieKey2);
				if(!!_hasOpened){
					delCookie(__cookieKey1,'lofter.com','/');
				} else{
					if(!!_doOpened){
						delCookie(__cookieKey1,'lofter.com','/');
						setCookie(__cookieKey2,'1','lofter.com',365,'/');
						$(document).ready(showRegLoginLayer);
					} else{
						setCookie(__cookieKey1,'1','lofter.com',365,'/');
					}
				}
			}
		};
		
		var setLoginFlag = function(_islogin){
			__isLogin = _islogin || false;
			var _loginFlag = '';
			if(__isLogin) _loginFlag = '1';
			setCookie(__cookieKey_loginFlag,_loginFlag,'lofter.com',1,'/');
			
			_dealOpenLogic();
		};
		window.setLoginFlag = setLoginFlag;
		
		
		
//		$('#__prev_permalink__').bind('click', function(event){
//			if(__isLogin) return;
//			var _doOpened = getCookie(__cookieKey1);
//			var _hasOpened = getCookie(__cookieKey2);
//			if(!_hasOpened){
//				setCookie(__cookieKey1,'1','lofter.com',365,'/');
//			} else{
//				delCookie(__cookieKey1);
//			}
//		});
//		
//		$('#__next_permalink__').bind('click', function(event){
//			if(__isLogin) return;
//			var _doOpened = getCookie(__cookieKey1);
//			var _hasOpened = getCookie(__cookieKey2);
//			if(!_hasOpened){
//				setCookie(__cookieKey1,'1','lofter.com',365,'/');
//			} else{
//				delCookie(__cookieKey1);
//			}
//		});
//		
//		var _doOpened = getCookie(__cookieKey1);
//		var _hasOpened = getCookie(__cookieKey2);
//		if(!!_hasOpened){
//			delCookie(__cookieKey1);
//			//refreshCookie();
//		} else{
//			if(!!_doOpened){
//				delCookie(__cookieKey1);
//				setCookie(__cookieKey2,'1','lofter.com',365,'/');
//				//refreshCookie();
//				$(document).ready(showRegLoginLayer);
//			}
//		}
		
		
	}

})();


