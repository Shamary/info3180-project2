// Your JavaScript Code here
var app=angular.module("project",['ngSanitize','mservice']);
app.controller("myCtlr",function($scope,$http,cflow){
    
    $scope.fname="";
    $scope.lname="";
    $scope.gender="M";
    $scope.age=0;
    $scope.uname="";
    $scope.password="";
    $scope.ispassword="";
    
    $scope.img_names=[];
    $scope.img_id=[];
    $scope.dets=[];
    $scope.url="";
    $scope.sav_url="";
    $scope.img_lst=[];
    $scope.wishlist=[];
    $scope.details="";
    
    $scope.iname="";
    
    $scope.window="";
    
    $scope.id="";
        
    $scope.to_addr="";
    $scope.to_name="";
    $scope.fro_addr="";
        
    $http.get("/gsession").then(function(result){
        //alert(result.data);
        $scope.id=result.data;
        
        $http.get("/api/users/"+$scope.id+"/wishlist").then(function(response){
        $scope.wishlist=response.data.urls;
        $scope.img_names=response.data.names;
        $scope.img_id=response.data.ids;
        $scope.dets=response.data.details;
        
        //alert($scope.wishlist[0]);
        
        });
    });

    
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
        }).then(function(result){
            //alert(result.data);
            window.location=result.data;
        });
    };
    
    $scope.fsubmit=function()
    {
        /*var data="fname= "+$scope.fname+"lname= "+$scope.lname+"gender= "+$scope.gender+"age= "+
        $scope.age+"uname= "+$scope.uname+"password= "+$scope.password;*/
        
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
            uname:$scope.uname,password:$scope.password,ispassword:$scope.ispassword}
        }).then(function(result){
            //alert(result.data);
            window.location=result.data;
        });
        /*.success(function(data,status,headers,config)
        {
           //alert(data); 
        })
        .error(function(data,status,headers,config)
        {
            //alert("failure: "+data);
        });
        
        $scope.reset();
        */
    };
    

    $scope.share=function()
    {
        $http({
            
            method:'POST',
            //http://info3180-project2-shamary.c9users.io:8080
            url:"/share",
            headers:{'Content-Type':'application/x-www-form-urlencoded'},
            transformRequest:function(obj){
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data:{to_addr:$scope.to_addr,to_name:$scope.to_name,from_addr:$scope.from_addr}
        }).then(function(result){
            //alert(result.data);
            window.location=result.data;
        });
    };

   
    
    $scope.getImg=function()
    {
        //alert($scope.img_lst[0]);
        /*$http.get("/api/thumbnails",{params:{'url':$scope.url}}).then(function(result){
            $scope.img_lst=result.data.thumbnails;
        });*/
        
        $scope.why_url=$scope.url;
        
        $http({
            
            method:'GET',
            url:"/api/thumbnails",
            
            params:{url:$scope.url}
        }).then(function(response){
            $scope.img_lst=response.data.thumbnails;
        });
        
        //$scope.bopt="<img ng-repeat='img in img_lst track by $index' src='{{img}}' class='col-md-4, img-thumbnail' width='120'></img>";
        //document.getElementById("opt").innerHTML="<img ng-repeat='img in img_lst track by $index' src={{img}} class='col-md-4'></img>";
    };
    
    $scope.add=function($event)
    {
        $scope.wishlist.push($event.target.value);
        
        cflow.wishlist=$scope.wishlist;
        
        $scope.url=$event.target.value;
        
        $http({
            
            method:'POST',
            url:"/api/users/"+$scope.id+"/wishlist",
            headers:{'Content-Type':'application/x-www-form-urlencoded'},
            transformRequest:function(obj){
                var str = [];
                for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data:{iname:$scope.iname,url:$scope.url,sav_url:$scope.sav_url,details:$scope.details}
        });
        
        //alert(cflow.wishlist[0]);
        //$scope.list_area="<img ng-repeat='item in wishlist track by $index' src='{{item}}' class='col-md-4'></img>"
        
        window.close($scope.window);
    };
    
    $scope.del_wish=function($event)
    {
        $scope.item_id=$event.target.value;
        $http.delete("/api/users/"+$scope.id+"/wishlist/"+$scope.item_id,"").then(function(result){
            window.location.reload();
        });
        //window.open("/api/users/"+$scope.id+"/wishlist/"+$event.target.value)
        
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
});

