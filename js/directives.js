angular.module('cartripsDirectives', []).
directive('loginDialog', function($timeout) {
   return {
       templateUrl: '/static/loginDialog.html',
       restrict: 'E',
       replace: true,
       controller: CredentialsController,
       link: function(scope, element, attributes, controller) {
           var isShowing = false;
           
           element.on('shown.bs.modal', function(e) {
               element.find('#userName').focus();
           });

           scope.$on('event:auth-loginRequired', function() {
               if (isShowing) {
                   return;
               }
               
               // If we're in the process of hiding the modal, we need to wait for
               // all CSS animations to complete before showing the modal again.
               // Otherwise, we might end up with an invisible modal, making the whole
               // view rather unusable. I've been unable to control the transitions
               // between "showing", "shown", "hiding", and "hidden" tightly using
               // JQuery notifications without collecting more and more modal backdrops
               // in the DOM, so the dirty solution here is to simply wait a second
               // before showing the log-in dialog.
               isShowing = true;
               $timeout(function() {
                   element.modal('show');
                   isShowing = false;
               }, 1000);
           });

           scope.$on('event:auth-loginConfirmed', function() {
               element.modal('hide');
               scope.credentials.password = '';
           });
       }
   } 
}).
directive('logoutLink', function() {
   return {
       templateUrl: '/static/logoutLink.html',
       restrict: 'E',
       replace: true,
       controller: LoginController
   } 
});
