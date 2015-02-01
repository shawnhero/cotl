/**
 * 提供给个性化页面使用的弹窗控件
 */
(function(){
var netease = window.netease || {};
window.netease = netease;
netease.lofter = {};
netease.lofter.widget = {};

var __ec = document.createDocumentFragment();

/**
 * @class netease.lofter.browser     判断浏览器
 */
var browser = netease.lofter.browser = function(){
    var agent = navigator.userAgent.toLowerCase(),
        opera = window.opera,
        browser = {
        /**
         * 检测浏览器是否为IE
         * @name netease.lofter.browser.ie
         * @property    检测浏览器是否为IE
         * @grammar     netease.lofter.browser.ie
         * @return     {Boolean}    返回是否为ie浏览器
         */
        ie		: !!window.ActiveXObject,

        /**
         * 检测浏览器是否为Opera
         * @name netease.lofter.browser.opera
         * @property    检测浏览器是否为Opera
         * @grammar     netease.lofter.browser.opera
         * @return     {Boolean}    返回是否为opera浏览器
         */
        opera	: ( !!opera && opera.version ),

        /**
         * 检测浏览器是否为WebKit内核
         * @name netease.lofter.browser.webkit
         * @property    检测浏览器是否为WebKit内核
         * @grammar     netease.lofter.browser.webkit
         * @return     {Boolean}    返回是否为WebKit内核
         */
        webkit	: ( agent.indexOf( ' applewebkit/' ) > -1 ),

        /**
         * 检查是否为Macintosh系统
         * @name netease.lofter.browser.mac
         * @property    检查是否为Macintosh系统
         * @grammar     netease.lofter.browser.mac
         * @return     {Boolean}    返回是否为Macintosh系统
         */
        mac	: ( agent.indexOf( 'macintosh' ) > -1 ),

        /**
         * 检查浏览器是否为quirks模式
         * @name netease.lofter.browser.quirks
         * @property    检查浏览器是否为quirks模式
         * @grammar     netease.lofter.browser.quirks
         * @return     {Boolean}    返回是否为quirks模式
         */
        quirks : ( document.compatMode == 'BackCompat' )
    };

    /**
     * 检测浏览器是否为Gecko内核，如Firefox
     * @name netease.lofter.browser.gecko
     * @property    检测浏览器是否为Gecko内核
     * @grammar     netease.lofter.browser.gecko
     * @return     {Boolean}    返回是否为Gecko内核
     */
    browser.gecko = ( navigator.product == 'Gecko' && !browser.webkit && !browser.opera );

    var version = 0;

    // Internet Explorer 6.0+
    if ( browser.ie )
    {
        version = parseFloat( agent.match( /msie (\d+)/ )[1] );

        /**
         * 检测浏览器是否为 IE8 浏览器
         * @name netease.lofter.browser.IE8
         * @property    检测浏览器是否为 IE8 浏览器
         * @grammar     netease.lofter.browser.IE8
         * @return     {Boolean}    返回是否为 IE8 浏览器
         */
        browser.ie8 = !!document.documentMode;

        /**
         * 检测浏览器是否为 IE8 模式
         * @name netease.lofter.browser.ie8Compat
         * @property    检测浏览器是否为 IE8 模式
         * @grammar     netease.lofter.browser.ie8Compat
         * @return     {Boolean}    返回是否为 IE8 模式
         */
        browser.ie8Compat = document.documentMode == 8;

        /**
         * 检测浏览器是否运行在 兼容IE7模式
         * @name netease.lofter.browser.ie7Compat
         * @property    检测浏览器是否为兼容IE7模式
         * @grammar     netease.lofter.browser.ie7Compat
         * @return     {Boolean}    返回是否为兼容IE7模式
         */
        browser.ie7Compat = ( ( version == 7 && !document.documentMode )
                || document.documentMode == 7 );

        /**
         * 检测浏览器是否IE6模式或怪异模式
         * @name netease.lofter.browser.ie6Compat
         * @property    检测浏览器是否IE6 模式或怪异模式
         * @grammar     netease.lofter.browser.ie6Compat
         * @return     {Boolean}    返回是否为IE6 模式或怪异模式
         */
        browser.ie6Compat = ( version < 7 || browser.quirks );

    }

    // Gecko.
    if ( browser.gecko )
    {
        var geckoRelease = agent.match( /rv:([\d\.]+)/ );
        if ( geckoRelease )
        {
            geckoRelease = geckoRelease[1].split( '.' );
            version = geckoRelease[0] * 10000 + ( geckoRelease[1] || 0 ) * 100 + ( geckoRelease[2] || 0 ) * 1;
        }
    }
    /**
     * 检测浏览器是否为chrome
     * @name netease.lofter.browser.chrome
     * @property    检测浏览器是否为chrome
     * @grammar     netease.lofter.browser.chrome
     * @return     {Boolean}    返回是否为chrome浏览器
     */
    if (/chrome\/(\d+\.\d)/i.test(agent)) {
        browser.chrome = + RegExp['\x241'];
    }
    /**
     * 检测浏览器是否为safari
     * @name netease.lofter.browser.safari
     * @property    检测浏览器是否为safari
     * @grammar     netease.lofter.browser.safari
     * @return     {Boolean}    返回是否为safari浏览器
     */
    if(/(\d+\.\d)?(?:\.\d)?\s+safari\/?(\d+\.\d+)?/i.test(agent) && !/chrome/i.test(agent)){
    	browser.safari = + (RegExp['\x241'] || RegExp['\x242']);
    }


    // Opera 9.50+
    if ( browser.opera )
        version = parseFloat( opera.version() );

    // WebKit 522+ (Safari 3+)
    if ( browser.webkit )
        version = parseFloat( agent.match( / applewebkit\/(\d+)/ )[1] );

    /**
     * 浏览器版本
     *
     * gecko内核浏览器的版本会转换成这样(如 1.9.0.2 -> 10900).
     *
     * webkit内核浏览器版本号使用其build号 (如 522).
     * @name netease.lofter.browser.version
     * @grammar     netease.lofter.browser.version
     * @return     {Boolean}    返回浏览器版本号
     * @example
     * if ( netease.lofter.browser.ie && <b>netease.lofter.browser.version</b> <= 6 )
     *     alert( "Ouch!" );
     */
    browser.version = version;

    /**
     * 是否是兼容模式的浏览器
     * @name netease.lofter.browser.isCompatible
     * @grammar     netease.lofter.browser.isCompatible
     * @return     {Boolean}    返回是否是兼容模式的浏览器
     * @example
     * if ( netease.lofter.browser.isCompatible )
     *     alert( "Your browser is pretty cool!" );
     */
    browser.isCompatible =
        !browser.mobile && (
        ( browser.ie && version >= 6 ) ||
        ( browser.gecko && version >= 10801 ) ||
        ( browser.opera && version >= 9.5 ) ||
        ( browser.air && version >= 1 ) ||
        ( browser.webkit && version >= 522 ) ||
        false );
    return browser;
}();

//快捷方式
var ie = browser.ie,
    webkit = browser.webkit,
    gecko = browser.gecko;

/**
 * 节点函数
 */
if (!window.Node){
    window.Node = {ELEMENT_NODE:1};
}

if (browser.gecko){
HTMLElement.prototype['__defineGetter__']("innerText",function(){return this.textContent;});
HTMLElement.prototype['__defineSetter__']("innerText",function(_content){this.textContent = _content;});
HTMLElement.prototype.insertAdjacentElement = function(_where,_element){
    if (!_where||!_element) return;
    switch(_where){
        case 'beforeEnd'  : this.appendChild(_element); return;
        case 'beforeBegin': this.parentNode.insertBefore(_element,this); return;
        case 'afterBegin' :
             !this.firstChild
             ?this.appendChild(_element)
             :this.insertBefore(_element,this.firstChild); return;
        case 'afterEnd'   :
             !this.nextSibling 
             ?this.parentNode.appendChild(_element)
             :this.parentNode.insertBefore(_element,this.nextSibling); return;
    }
};
HTMLElement.prototype.insertAdjacentHTML = function(_where,_html){
    if (!_where||!_html) return;
    this.insertAdjacentElement(_where,
         document.createRange().
         createContextualFragment(_html));
};}

/**
 * 绑定接口及参数，使其的调用对象保持一致
 * @param  {Object}   _object 需要保持一致的对象，null表示window对象
 * @param  {Variable} [argument0[,argument1 ...]] 函数调用时需要的参数
 * @return {Function} 返回绑定后的函数
 */
Function.prototype._$bind = function() {
    var _args = arguments,
        _object = arguments[0],
        _function = this;
    return function(){
        // not use slice for chrome 10 and Array.apply for android
        var _argc = [].slice.call(_args,1);
        [].push.apply(_argc,arguments);
        return _function.apply(_object||window,_argc);
    };
};

/**
 * 工具集对象
 */
var utils = netease.lofter.utils = {
		
	//去掉字符串前后的空白
	trim : function(_str) {
		if(_str!=null) {
			return _str.replace(/(^\s*)|(\s*$)/g, "");
		} else {
			return null;
		}
	},
	
	stopBubble : function(_event) {
		_event = _event ? _event : window.event;
		if(!_event) return;
		if(!!(window.attachEvent &&!window.opera)) {
			_event.cancelBubble = true;
		} else {
			_event.stopPropagation();
		}
		return _event;
	},
	
	stopDefault: function(_event){
		if (!_event) return;
	    !!_event.preventDefault
	    ? _event.preventDefault()
	    : _event.returnValue = false;
	},
	
	stopEvent : function(_event){
		this.stopBubble(_event);
		this.stopDefault(_event);
	},
	
	addEvent : function(_element,_type,_handler,_capture){
		_element = this.getElement(_element);
		if (!_element||!_type||!_handler) return;
		if (!!document.addEventListener) {
			_element.addEventListener(_type,_handler,!!_capture);
		}else{
			_element.attachEvent('on'+_type,_handler);
		}
	},
	
	delEvent : function(_element,_type,_handler,_capture){
		 _element = this.getElement(_element);
		if (!_element||!_type||!_handler) return;
		if (!!document.addEventListener) {
			_element.removeEventListener(_type,_handler,!!_capture);
		}else{
			_element.detachEvent('on'+_type,_handler);
		}
	},
	
	//执行正则式
	isExpectedString : function(pattern,str){
		if(pattern.test(str)) {		
			return true;
		} else{
			return false;
		}
	},
	
	//判断某节点是否包含指定class
	hasClassName : function(_element,_classname){
		_classname = this.trim(_classname);
		if(!_element || !_element.className || !_classname) return false;
		
		var _classnamepattern = "\\s+" + _classname + "\\s+";
		var _reg = new RegExp(_classnamepattern);
		return this.isExpectedString(_reg," "+ _element.className +" ")
	},
	
	/**
	 * 获取节点的element子节点，不计算非ELEMENT_NODE的节点
	 * @param  {String|Node} _element 节点ID或者对象
	 * @param  {String}      _class   筛选节点的样式名称
	 * @return {Array} 子节点列表
	 */
	getChildElements : function(_element,_class){
	    _element = this.getElement(_element);
	    if (!_element) return null;
	    var _result = [];
	    for(var _node=_element.children||
	        _element.childNodes,i=0,l=_node.length;i<l;i++){
	        if (_node[i].nodeType!=Node.ELEMENT_NODE||
	           (_class&&!this.hasClassName(_node[i],_class))) continue;
	        _result.push(_node[i]);
	    }
	    return _result;
	},
	
	//通过className 取得dom元素
	getElementsByClassName : function(_fatherobj,_classname){
		var _element = [];
		_fatherobj = utils.getElement(_fatherobj);

		if(typeof _fatherobj != "object" || _fatherobj == null){
			_fatherobj = document;
		}
	
		var _el = _fatherobj.getElementsByTagName('*');
		
		for (var i=0; i<_el.length; i++ ) {
			if(this.hasClassName(_el[i],_classname)){
				_element[_element.length] = _el[i];
			}
		}
		return _element;
	},
	
	//addClassName
    addClassName : function(_obj,_classname) {
		if(!this.hasClassName(_obj,_classname)){
			_obj.className = _obj.className + " " + _classname;
		}
	},
	
	//delClassName
	delClassName : function(_obj,_classname) {
		if(!!this.hasClassName(_obj,_classname)){
			var _classnamepattern = "(^" + _classname + "\\s+)" + "|" + "(\\s+" + _classname + "\\s+)"  + "|" + "(\\s+" + _classname + "$)";
			var _reg = new RegExp(_classnamepattern,'g');
			_obj.className = _obj.className.replace(_reg, " ");
		}
	},
	
	/**
	 * 从页面删除节点并回收内存空间
	 * @param  {String|Node} _element 节点ID或者对象
	 * @return {Void}
	 */
	removeElement : function(_element){
		_element = this.getElement(_element);
	    if (!_element||!_element.parentNode) return;
	    _element.parentNode.removeChild(_element);
	    if(browser.ie&&!!_element.outerHTML) _element.outerHTML = '';
	    // ie: mem leak if any child has event listener not detach
	},
	
	/**
	 * 从页面删除节点，放至内存空间，防止节点被回收
	 * @param  {String|Node} _element 要删除的节点ID或者对象
	 * @return {Void}
	 */
	removeElementByEC : function(){
	    for(var i=0,l=arguments.length,_element;i<l;i++){
	        _element=utils.getElement(arguments[i]);
	        _element&&__ec.appendChild(_element);
	    }
	},
	
	getElement : function(_element){
		if(typeof _element == 'string' || typeof _element == 'number'){
			_element = document.getElementById(_element);
		}
		return _element;
	}
	
};

var pageLayer = netease.lofter.widget.pageLayer = function(){};
pageLayer._$getInstance = function(_parent,_options){
    if (!!this.__instance){
        this.__instance.resetOption(_options);
    } else{
    	this.__instance = new this();
    	this.__instance.init(_parent,_options);
    }
    return this.__instance
};

pageLayer.prototype = {	
	init : function(_parent,_options){
	    this.__body = document.createElement('div');
	    this.__body.className = this.getSpace();
		this.__body.innerHTML = this.getXhtml();
		this.initNode();
		
		this.reset(_parent,_options);
		
		utils.addEvent(window, 'resize', this.resizewin._$bind(this,false));
		
		utils.addEvent(document.body, 'click', this.onDocumentClick._$bind(this));

	},
	
	onDocumentClick : function(_event){
		if(!this.__noDocClickDestroy){
			//标签归档通过cbBeforeDestroy来实现关闭浮层,destroy方法写在cbBeforeDestroy里面
			if(!!this.cbBeforeDestroy){
				this.cbBeforeDestroy();
			}else{
				this.destroy();
			}
		}
	},
	
	onKeyPress : function(_event){
		var _code = _event.keyCode;
		if(_code==38 || _code==40){
			//utils.stopEvent(_event);
			if(!this.destroyed() && this.__hasKeyEvent){
				utils.stopDefault(_event);
			}
		}
	},
	
	getSpace : function(){
		return 'w-pagelayer';
	},
	
	getXhtml : function(){
		return '<div class="pagelayer ztag">\
		            <div class="lyloading a-scale ztag"></div>\
		            <div class="lycover a-scale ztag">&nbsp;</div>\
		            <div class="lyscroll ztag">\
		                <a href="#" class="lyclosed ztag"></a>\
		                <div class="lybody ztag">\
		                    <div class="lycont a-scale ztag"></div>\
		                </div>\
		            </div>\
		        </div>'
	},
	
	initNode : function(){
		var _ntmp = utils.getElementsByClassName(this.__body,'ztag');
		var _index = 0;
		this.__pagelayer = _ntmp[_index++];
		this.__lyloading = _ntmp[_index++];
		this.__lycover = _ntmp[_index++];
		this.__lyscroll = _ntmp[_index++];
		this.__lyclosed = _ntmp[_index++];
		this.__lybody = _ntmp[_index++];
		this.__lycont = _ntmp[_index++];
		
		utils.addEvent(this.__lycont,'click',this.onLycontClick._$bind(this));
		utils.addEvent(this.__lyclosed,'click',this.onClosedClick._$bind(this));
	},
	
	onLycontClick : function(_event){
		if(!this.__noDocClickDestroy) {
		    utils.stopBubble(_event);
		}
		
		if(browser.gecko && !!this.__hasKeyEvent){
			utils.delEvent(document.body, 'keydown', this.onKeyPress._$bind(this));
			this.__hasKeyEvent = false;
		}
	},
	
	onClosedClick : function(_event){
		utils.stopEvent(_event);
		this.destroy();
	},
	
	reset : function(_parent,_options){
		_options = _options || {};
		_parent = utils.getElement(_parent);
	    this.__parent = _parent==document.documentElement?document.body:_parent;
	    
		this.resetOption(_options);
		
		//禁用firefox系列浏览器的向上，向下键
		if (browser.gecko && !this.__hasKeyEvent){
			this.__hasKeyEvent = true;
			utils.addEvent(document.body, 'keydown', this.onKeyPress._$bind(this));
		}
	},
	
	resetOption : function(_options){
		//显示加载中图标
		//this.__lyloading.style.visibility = 'visible';
		utils.addClassName(this.__lyloading,'a-scale-do');
		
		if(!!_options.showClosedIcon){
			this.__lyclosed.style.display = 'block';
		} else{
			this.__lyclosed.style.display = '';
		}
		
		this.__pagelayer.style.zIndex = _options.zIndex || '';
		
		//是否需要启用内容区最小高度算法
		this.__notSetContMinHeight = _options.notSetContMinHeight || false;
		
		//是否启用点击document区域销毁控件
		this.__noDocClickDestroy = _options.noDocClickDestroy || false;
		
		this.__isNeedAnimation = (!browser.ie && _options.isNeedAnimation) || false;
		this.__class = _options['class']||'';
		utils.addClassName(this.__body,this.__class);
		this.cbAfterSetHtmlContent = _options.cbAfterSetHtmlContent;
		this.cbAfterDestroy = _options.cbAfterDestroy;
		if(!this.__used){
		    this.hideScroll();
		    //将控件实体放到文档的parent节点中
		    this.appendToParent(!!_options.before);
		}
		this.showCover(_options.bgcolor,_options.opacity);
		
		this.setHtmlContent(_options.html);
		
	},
	
	getNoDocClickDestroy : function(){
		return this.__noDocClickDestroy;
	},
	
	setNoDocClickDestroy : function(_noDocClickDestroy){
		this.__noDocClickDestroy = _noDocClickDestroy || false;
	},
	
	hideScroll : function(){
		
		var _body0 = document.documentElement || document.body;
		
		//禁用滚动条，这里保存页面滚动值，用来恢复页面滚动区
		this.__scrollTop = window.pageYOffset//FF
	                || document.documentElement.scrollTop  
	                || document.body.scrollTop  
	                || 0;
	    
	    this.__bodyOverflowY = _body0.style.overflowY;
	    var _oldClientWidth = _body0.clientWidth || 0;
		_body0.style.overflowY = 'hidden';
		//修正滚动条隐藏后的body区实际宽度变化
		var _clientWidth = _body0.clientWidth || 0;
		if(_clientWidth>_oldClientWidth){
			_body0.style.paddingRight = (_clientWidth - _oldClientWidth) + 'px';
		}
		
		this.__bodyOverflowX = _body0.style.overflowX;
		_body0.style.overflowX = 'hidden';
		//重新计算这个值是因为FF在禁用滚动条后,页面滚到顶部了
		this.__scrollTopNow = window.pageYOffset//FF
	                || document.documentElement.scrollTop  
	                || document.body.scrollTop  
	                || 0;
	},
	
	setHtmlContent : function(_html){
		//设置前
		//显示loaing图标
	    //this.__lyloading.style.visibility = '';
	    utils.addClassName(this.__lyloading,'a-scale-do');
		
		this.beforeSetHtmlContent(_html);
		//设置
		if(!!this.__isNeedAnimation && !!this.__lycont.innerHTML){
			this.doAnimate(true);
			window.setTimeout(this.doSetHtmlContent._$bind(this,_html),280);
		} else{
			this.doSetHtmlContent(_html);
		}
		
	},
	
	beforeSetHtmlContent : function(_html){
		if(!!_html && browser.ie){
			this.__lycont.style.visibility = 'hidden';
		}
	},
	
	doSetHtmlContent : function(_html){
		this.__lycont.innerHTML = _html || '';
		//设置后
		this.afterSetHtmlContent(_html);
		//设置后的回调（供调用者使用）
		if(!!this.cbAfterSetHtmlContent) this.cbAfterSetHtmlContent(this.__lycont);
	},
	
	
    afterSetHtmlContent : function(_html){
		//此行十分关键，保证resetOption 时，内容置空时不触发一下动画和最小高度计算。保持内容为空的状态下整个内容区为透明状态
		//切加载中图标为显示状态
		if(!_html) return;
		
		if(!!_html &&  browser.ie){
			window.setTimeout(this.setZoomForIE._$bind(this),300);
		}
		
		if(!!this.__isNeedAnimation){
			//此处的延时是用来等待加载图片之类的
			window.setTimeout(this.doAnimate._$bind(this),200);
			//this.doAnimate();
		} else{
			this.doAnimate();
		}
		
		//设置内容区最小高度
		this.setLyContMinHeight();
		
		//隐藏loading图标
		//this.__lyloading.style.visibility = 'hidden';
		utils.delClassName(this.__lyloading,'a-scale-do');
		
	},
	
	
	doAnimate : function(_isClose){
		if(!_isClose){
			utils.addClassName(this.__lycont,'a-scale-do');
		} else{
			utils.delClassName(this.__lycont,'a-scale-do');
		}
	},
	
	//当页面高度小于3/4个屏幕时，设置页面的最小高度为3/4个屏幕
	setLyContMinHeight : function(){
		if(!!this.__notSetContMinHeight){
			//配置参数指定不需要计算最小高度
			return;
		}
		
		if(!this.__lycont.innerHTML){
			return;
		}
		if(!!this.__setMinHeightTimer) this.__setMinHeightTimer = window.clearTimeout(this.__setMinHeightTimer);
		this.__setMinHeightTimer = window.setTimeout(this.doLyContMinHeight._$bind(this),10);
	},
	
	doLyContMinHeight : function(){
		if(this.destroyed()) return;
		var _body = document.documentElement||document.body;
		var _clientHeight = _body.clientHeight || 1;
		
		var _children = utils.getChildElements(this.__lycont);
		var _firstChild;
		//理论上this.__lycont只能有一个子节点
		if(!!_children && _children.length==1){
			_firstChild = _children[0];
		}
		
		if (browser.ie6Compat){
			if(!!_firstChild){
				_firstChild.style.height = 'auto';
			} else{
				this.__lycont.style.height = 'auto';
			}
		} else{
		    if(!!_firstChild){
		    	_firstChild.style.minHeight = 0;
		    } else{
		    	this.__lycont.style.minHeight = 0;
		    }
		}
		//恢复lycont节点的高度为 auto
		//this.__lycont.style.height = 'auto';
		
		var _lycontHeight = this.__lycont.clientHeight || 1;
		var _minContHeight = Math.ceil(_clientHeight*3/4);
		if(_minContHeight>_lycontHeight){
			if (browser.ie6Compat){
				if(!!_firstChild){
					_firstChild.style.height = _minContHeight + 'px';
				} else{
					this.__lycont.style.height = _minContHeight + 'px';
				}
			} else{
				if(!!_firstChild){
					_firstChild.style.minHeight = _minContHeight + 'px';
				} else{
					this.__lycont.style.minHeight = _minContHeight + 'px';
					//this.__lycont.style.height = _minContHeight + 'px';
				}
			 
			}
		}
	},
	
	//修复ie下某些绝对定位位置有偏差，鼠标移上去抖一下后才恢复到正常位置
	setZoomForIE : function(){
		this.__body.style.zoom = 1;
		this.__lycont.style.visibility = 'visible';
	},
	
	
	showCover : function(_bgcolor,_opacity){
		this.resizewin(true);
		if(browser.ie){
			window.setTimeout(this.showCoverForIE._$bind(this),10);
		} else{
			this.__lycover.style.visibility = 'visible';
		}
		
		this.__bgcolor = _bgcolor;
		this.__opacity = _opacity;
		if(!!_bgcolor){
			this.__lycover.style.backgroundColor = _bgcolor;
		} else{
			this.__lycover.style.backgroundColor = '';
		}
		if(!!_opacity || _opacity===0){
			this.__lycover.style.opacity = _opacity/100;
			this.__lycover.style.filter = 'alpha(opacity=' + _opacity + ')';
		} else{
			this.__lycover.style.opacity = '';
			//this.__lycover.style.filter = '';
		}
		
	},
	
	//此方法是为了实现渐隐 动画
	hideCover : function(){
		if(browser.ie){
			this.__lycover.style.visibility = 'hidden';
		} else{
			this.__lycover.style.opacity = 0;
		}
	},
	
	showCoverForIE : function(){
		this.__lycover.style.visibility = 'visible';
	},

	resizewin : function(_isFromShowCover){
		if(!_isFromShowCover){
		    this.setLyContMinHeight();
	    }
		
		if (browser.ie6Compat){
	        var _body = document.documentElement||document.body;
	        //this.__lycover.style.width  = _body.scrollWidth+'px';
	        //this.__lycover.style.height = _body.scrollHeight+'px';
	        
	        this.__lycover.style.width  = _body.clientWidth+'px';
	        this.__lycover.style.height = _body.clientHeight+'px';
	        
	        this.__lyscroll.style.width  = _body.clientWidth+'px';
	        this.__lyscroll.style.height =  _body.clientHeight+'px';
	        
	        this.__pagelayer.style.width  = _body.clientWidth+'px';
	        this.__pagelayer.style.height =  _body.clientHeight+'px';
	        this.__pagelayer.style.top = this.__scrollTopNow || 0 + 'px';
	        
	    }
		
	},
	
	appendToParent : function(_before){
	    if (!this.__body) return;
	    this.revertBody(_before);
	},
	
	/**
	 * 恢复控件节点
	 * @param  {String|Node} _parent 父节点ID或者对象
	 * @param  {Boolean}     _before 是否在父节点的第一个位置
	 * @return {Void}
	 */
	 revertBody : function(_before){
	    if (!this.__parent||!this.__body) return;
	    !_before ? this.__parent.appendChild(this.__body)
	             : this.__parent.insertAdjacentElement('afterBegin',this.__body);
	    this.__used = true;
	},
	
    destroy : function(){
		if(browser.gecko && !!this.__hasKeyEvent){
			utils.delEvent(document.body, 'keydown', this.onKeyPress._$bind(this));
			this.__hasKeyEvent = false
		}
		if(!this.destroyed()){
			//关闭时的动画
			//this.__lyloading.style.visibility = 'hidden';
			utils.delClassName(this.__lyloading,'a-scale-do');
			if(!!this.__isNeedAnimation){
				//销毁此控件实体时，遮罩的渐隐动画
				this.hideCover();
				this.doAnimate(true);
				window.setTimeout(this.recycleBody._$bind(this),280);
			} else{
			    this.recycleBody();
			}
		}
		//此控件销毁后的回调
		if(!!this.cbAfterDestroy) this.cbAfterDestroy();
	},
	
	destroyed : function(){
    	return !this.__used;
	},
	
	/**
	 * 回收控件节点
	 * @return {Void}
	 */
	recycleBody : function(){
		this.__used = false;
	    utils.removeElementByEC(this.__body);
	    this.__lycont.innerHTML = '';
	    this.recoverScroll();
	},
	
	recoverScroll : function(_event){
		utils.stopEvent(_event);
		
		var _body0 = document.documentElement || document.body;
		
		//修正滚动条恢复后的body区实际宽度变化
		_body0.style.paddingRight = 0;
		
		_body0.style.overflowY =  this.__bodyOverflowY || '';//禁用滚动条结束，恢复overflowY的CSS样式
		_body0.style.overflowX =  this.__bodyOverflowX || '';//禁用滚动条结束，恢复overflowY的CSS样式
		document.documentElement.scrollTop=document.body.scrollTop=this.__scrollTop;
		
	}
	
};

})();