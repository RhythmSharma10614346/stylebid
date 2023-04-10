<?php
$conn = mysqli_connect("localhost", "root", "");
if(isset($_POST['login_btn'])){
    $username=$_POST('username');
    $username=$_POST('password');
    $sql= "SELECT * FROM stylebid.logindetails WHERE username = '$username'";
    $result = mysqli_query($conn,$sql);
    while($row = mysql_fetch_assoc($result)){
        $resultPassword = $row['password'];
        if($password == $resultPassword){
            header('Location:auction.html');
        }
        else
            echo {
                alert('Login failed, Try again')
            }
                
        }
    }


?>