// Your JavaScript Code here
var app=angular.module("project",[]);
app.controller("myCtlr",function($scope,$http){
    /*$http.post("http://info3180-lab7-shamary.c9users.io:8080/api/thumbnails","")
    .then(function(result){
        $scope.img_lst=result.data.thumbnails;
        
        //alert(result.data.thumbnails);
    });*/
    $scope.fname="";
    $scope.lname="";
    $scope.gender="M";
    $scope.age=0;
    $scope.uname="";
    $scope.password="";
    $scope.ispassword="";
    
    $scope.reset=function()
    {
        $scope.fname="";
        $scope.lname="";
        $scope.gender="M";
        $scope.age=0;
        $scope.uname="";
        $scope.password="";
        $scope.ispassword="";
    }
    
    $scope.fsubmit=function()
    {
        var data="fname= "+$scope.fname+"lname= "+$scope.lname+"gender= "+$scope.gender+"age= "+
        $scope.age+"uname= "+$scope.uname+"password= "+$scope.password;
        
        $http({
            
            method:'POST',
            url:"http://info3180-project2-shamary.c9users.io:8080/api/users/register",
            headers:{'Content-Type':'application/x-www-form-urlencoded'},
            transformRequest:function(obj){
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data:{fname:$scope.fname,lname:$scope.lname,gender:$scope.gender,age:$scope.age,
            uname:$scope.uname,password:$scope.password}
        })
        .success(function(data,status,headers,config)
        {
           //alert(data); 
        })
        .error(function(data,status,headers,config)
        {
            //alert("failure: "+data);
        });
        
        $scope.reset();
    };
});