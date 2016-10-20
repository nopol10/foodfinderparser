<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Food Finder</title>

    <!-- Bootstrap core CSS -->
    <link href="./docs/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="./docs/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="starter-template.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="./docs/assets/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Food Finder</a>
        </div>
      </div>
    </nav>

    <div class="container">

      <div class="starter-template">
        <h1>Food Finder</h1>
        <p class="lead">Search for restaurants according to your preferences.</p>
      </div>

			<div class="container">
  				<label class="sr-only" for="exampleInputEmail3">Search:</label>
    				<input type="text" name="search" id="search">
				<button id="searchButton" type="button" onclick="sendToPhp();">submit</button>
				<!-- <select class="form-control">
  				<option>Name</option>
  				<option>Country</option>
				</select> -->	
			</div>
			
			<div class="container">

		<!--	<?php
			
		function displayResult($name){
			// Connect to database server
			mysql_connect("localhost", "foodfinder", "foodfinder");

			// Select database
			mysql_select_db("foodfinder");

			// SQL query
			$strSQL = "SELECT $result FROM restaurants";

			// Execute the query (the recordset $rs contains the result)
			$rs = mysql_query($strSQL);
	
			// Loop the recordset $rs
			// Each row will be made into an array ($row) using mysql_fetch_array
			while($row = mysql_fetch_array($rs)) {

	   	// Write the value of the column FirstName (which is now in the array $row)
	  	echo $row['FirstName'] . "<br />";
	  	}

			// Close the database connection
			mysql_close();}
			?>-->
			</div>
    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	<script>
      function sendToPhp(){
	var search = document.getElementById("search");	 
	document.getElementById("search").value = "";
	$.ajax({
	  type: "POST",
	  url: "foodfinder.php",
	  data: { name: search }
	}).done(function( msg ) {
	  alert( "Data Saved: " + msg );
	});  

	}
	</script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="./dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="./assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>

