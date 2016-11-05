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
    <link href="dist/css/bootstrap.min.css" rel="stylesheet">

    <!--Foodfinder CSS-->
    <link href="https://fonts.googleapis.com/css?family=Lobster+Two" rel="stylesheet">
    <link href="dist/css/ffstyle.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="./docs/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="starter-template.css" rel="stylesheet">

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
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar"
                    aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#">Food Finder</a>
        </div>
    </div>
</nav>

<div class="starter-template background-banner">
    <h1 class="title">Food Finder</h1>
    <h2 class="">Find restaurants based on your preferences.</h2>
</div>
<div class="container main-panel">
        <button class="btn-lg btn btn-success" type="button" onclick="searchByName(true);">Show Food Near Me!</button>
        <button class="btn-lg btn btn-primary" type="button" onclick="showSearchBar();">I want something specific!</button>

        <div id="search-panel">
            <input type="text" name="search" class="form-control ff-searchbar" placeholder="Enter a type of food, location or name" id="search">
            <button id="searchButton" class="btn btn-success" type="button" onclick="searchByName(false);">I'm Hungry!</button>
        </div>

        <!-- <select class="form-control">
          <option>Name</option>
          <option>Country</option>
        </select> -->

    <div id='restaurant-container'>

    </div>
</div><!-- /.container -->


<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>

</script>
<script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
<script src="./dist/js/bootstrap.min.js"></script>
<script src="dist/js/scripts.js"></script>
<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="./assets/js/ie10-viewport-bug-workaround.js"></script>
</body>
</html>

