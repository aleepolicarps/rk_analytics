'use strict';

var RK_ANALYTICS_URL = 'http://rk-analytics-env.fksdxdtg32.ap-southeast-1.elasticbeanstalk.com';

window.rkAnalytics = {};

var guid = function () {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

var getSession = function() {
  if(localStorage.getItem('session')) {
    return localStorage.getItem('session');
  } else {
    var session = guid();
    localStorage.setItem('session', session);
    return session;
  }
}

var getUrlParameters = function(url){
  var pairs = url.substring(url.indexOf('?') + 1).split('&');
  var params = {};
  for(var i = 0; i < pairs.length; i++) {
      if(!pairs[i]) {
        continue;
      }

      var pair = pairs[i].split('=');
      params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
  }

  return params;
};

window.rkAnalytics.trackUserAction = function(action, section = '', subsection = '', value = '') {
  var urlParams = getUrlParameters(window.location.href);

  $.ajax({
    url: RK_ANALYTICS_URL + '/events/user-action',
    data: {
      account: window.location.hostname,
      action: action,
      customer_id: window.gbl_new_user_id === undefined ? null : window.gbl_new_user_id,
      web_id: $('#webid').val(),
      first_name: $('#fname').val(),
      last_name: $('#lname').val(),
      email: $('#email').val(),
      session: getSession(),
      section: section,
      subsection: subsection,
      value: value,
      utm_source: urlParams['utm_source'],
      utm_medium: urlParams['utm_medium'],
      utm_campaign: urlParams['utm_campaign'],
      utm_content: urlParams['utm_content'],
      utm_term: urlParams['utm_term'],
    }
  });
};
