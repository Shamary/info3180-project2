// Your JavaScript Code here
var app=angular.module("project",['ngSanitize','mservice']);
app.controller("myCtlr",function($scope,$http,cflow){
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
    
    $scope.url="";
    $scope.img_lst=[];
    $scope.wishlist=[];
    
    $scope.iname=""
    
    $scope.window="";
    
    $scope.reset=function()
    {
        $scope.fname="";
        $scope.lname="";
        $scope.gender="M";
        $scope.age=0;
        $scope.uname="";
        $scope.password="";
        $scope.ispassword="";
    };
    
    $scope.login=function()
    {
        $http({
            
            method:'POST',
            url:"/api/users/login",
            headers:{'Content-Type':'application/x-www-form-urlencoded'},
            transformRequest:function(obj){
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data:{uname:$scope.uname,password:$scope.password}
        });
    }
    
    $scope.fsubmit=function()
    {
        var data="fname= "+$scope.fname+"lname= "+$scope.lname+"gender= "+$scope.gender+"age= "+
        $scope.age+"uname= "+$scope.uname+"password= "+$scope.password;
        
        $http({
            
            method:'POST',
            //http://info3180-project2-shamary.c9users.io:8080
            url:"/api/users/register",
            headers:{'Content-Type':'application/x-www-form-urlencoded'},
            transformRequest:function(obj){
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data:{fname:$scope.fname,lname:$scope.lname,gender:$scope.gender,age:$scope.age,
            uname:$scope.uname,password:$scope.password}
        });
        /*.success(function(data,status,headers,config)
        {
           //alert(data); 
        })
        .error(function(data,status,headers,config)
        {
            //alert("failure: "+data);
        });*/
        
        $scope.reset();
    };
    
   
    
    $scope.getImg=function()
    {
        //alert($scope.img_lst[0]);
        /*$http.get("/api/thumbnails",{params:{'url':$scope.url}}).then(function(result){
            $scope.img_lst=result.data.thumbnails;
        });*/
        
        
        $http({
            
            method:'GET',
            url:"/api/thumbnails",
            
            params:{url:$scope.url}
        })
        .then(function(response){
            $scope.img_lst=response.data.thumbnails;
        });
        
        //$scope.bopt="<img ng-repeat='img in img_lst track by $index' src='{{img}}' class='col-md-4, img-thumbnail' width='120'></img>";
        //document.getElementById("opt").innerHTML="<img ng-repeat='img in img_lst track by $index' src={{img}} class='col-md-4'></img>";
    };
    
    $scope.add=function($event)
    {
        $scope.wishlist.push($event.target.value);
        
        cflow.wishlist=$scope.wishlist;
        
        //alert(cflow.wishlist[0]);
        //$scope.list_area="<img ng-repeat='item in wishlist track by $index' src='{{item}}' class='col-md-4'></img>"
        
        window.close($scope.window);
    }
});

app.controller("myCtlr2",function($scope,$http,cflow){
    
    $scope.flow=cflow;
    //$scope.wishlist=cflow.wishlist;
    
     $scope.open=function()
    {
        //alert($scope.flow.wishlist[0]);
        $scope.window=window.open("/addItem","","width=700,height=600,top=15,left=30");
    };
    
});

var mservice=angular.module('mservice',[]).service('cflow',function(){
    this.wishlist=[];
})