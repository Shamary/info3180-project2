// Your JavaScript Code here
var app=angular.module("thumbnail",[]);
app.controller("myCtlr",function($scope,$http){
    $http.post("http://info3180-lab7-shamary.c9users.io:8080/api/thumbnails","")
    .then(function(result){
        $scope.img_lst=result.data['thumbnails'];
        
        alert(result.data['thumbnails']);
    });
});