var agent = navigator.userAgent.toLowerCase();
if ( (navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1) || (agent.indexOf('edge/') > -1)) {
    alert("Reborn Web은 Internet Explorer 또는 Edge에 최적화되어 있지 않습니다. Google Chrome과 같은 타 브라우저를 이용해주세요.");
}