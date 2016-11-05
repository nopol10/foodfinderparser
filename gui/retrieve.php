<?php
/**
 * @param $name
 */

function retrieveResults($type, $auto) {
    $conn = new mysqli("localhost", "foodfinder", "foodfinder", "foodfinder");
    $strSQL = "SELECT restaurant_name, country, web_rating, address, average_price, source_website, food_type FROM restaurants ";
    if ($auto == 'yes') {
        $statement = prepareCountryStatement($conn, 'AUTO');
    } else {
        $statement = prepareGeneralSearchStatement($conn, $type);
    }
    displayResultNew($statement);

}

function prepareGeneralSearchStatement($conn, $type) {
    $strSQL = "SELECT restaurant_name, country, web_rating, address, average_price, source_website, food_type FROM restaurants 
                WHERE food_type LIKE ? OR restaurant_name LIKE ?
                OR address LIKE ?
                ORDER BY web_rating DESC 
               LIMIT 10";
    $type = "%" . strtolower($type) . "%";
    if ($statement = $conn->prepare($strSQL)) {
        $statement->bind_param("sss", $type, $type, $type);
        $statement->execute();
//        $statement->bind_result($resName, $resCountry, $resWebRating, $resAddress, $resPrice, $resWebsite, $resFoodType);
        return $statement;
    }
}

function prepareCountryStatement($conn, $country) {
    if ($country == 'AUTO') {
        $user_ip = getenv('REMOTE_ADDR');
//        $geo = unserialize(file_get_contents("http://www.geoplugin.net/php.gp?ip=167.181.193.222"));
        $geo = unserialize(file_get_contents("http://www.geoplugin.net/php.gp?ip=$user_ip"));
        $country = $geo["geoplugin_countryName"];
//        $city = $geo["geoplugin_city"];
    }
    $strSQL = "SELECT restaurant_name, country, web_rating, address, average_price, source_website, food_type FROM restaurants 
                WHERE country LIKE ?";
    $country = "%" . strtolower($country) . "%";
    if ($statement = $conn->prepare($strSQL)) {
        $statement->bind_param("s", $country);
        $statement->execute();
        return $statement;
    }
}

function displayResultNew($statement) {
    $statement->bind_result($resName, $resCountry, $resWebRating, $resAddress, $resPrice, $resWebsite, $resFoodType);
    while ($statement->fetch()) {
        $resCountry = ucfirst($resCountry);
        $resWebRating = $resWebRating * 100;
        $resPrice = '$' . $resPrice;
//            $outArray[] = array('name' => $resName, 'country' => $resCountry, 'webrating' => $resWebRating, 'address' => $resAddress,
//                'price' => $resPrice);

        $allTypes = explode(',', $resFoodType);
        echo "<div class='restaurant-listing'>
                    <div class='res-name'><a href='$resWebsite'>$resName</a></div>
                    <div class='res-country'>$resCountry</div>
                    <div class='res-webrating'>$resWebRating</div>
                    <div class='res-address'>$resAddress</div>
                    <div class='res-types'>
                    ";
        foreach ($allTypes as $singleType) {
            $singleType = ucwords($singleType);
            echo "<span class='tag label label-info'>$singleType</span>";
        }
        echo "</div>";

        if (strlen($resPrice) > 1) {
            echo "<div class='res-price'>$resPrice</div>";
        } else {
            echo "<div class='res-price invisible'>0</div>";
        }
        echo "</div>";
    }
}

function displayResult($type, $auto)
{
    // Connect to database server
    $conn = new mysqli("localhost", "foodfinder", "foodfinder", "foodfinder");

    // Get user's country
    $user_ip = getenv('REMOTE_ADDR');
    $geo = unserialize(file_get_contents("http://www.geoplugin.net/php.gp?ip=167.181.193.222"));
    $country = $geo["geoplugin_countryName"];
    $city = $geo["geoplugin_city"];

//    echo "You are in ".$country;

    // Select database

    // Process food type
    $type = "%" . strtolower($type) . "%";
    // SQL query
    $strSQL = "SELECT restaurant_name, country, web_rating, address, average_price, source_website, food_type FROM restaurants ";
    if ($auto == 'yes') {
        $strSQL .= "WHERE country LIKE ?";
    } else {
        $strSQL .= "WHERE food_type LIKE ? OR restaurant_name LIKE ?
                OR address LIKE ?
                ORDER BY web_rating DESC 
               LIMIT 10";
    }

    // Execute the query (the recordset $rs contains the result)
    if ($statement = $conn->prepare($strSQL)) {
        $statement->bind_param("sss", $type, $type, $type);
        $statement->execute();
        $statement->bind_result($resName, $resCountry, $resWebRating, $resAddress, $resPrice, $resWebsite, $resFoodType);
        $i = 0;
        $outArray = array();
        while ($statement->fetch()) {
            $resCountry = ucfirst($resCountry);
            $resWebRating = $resWebRating * 100;
            $resPrice = '$' . $resPrice;
//            $outArray[] = array('name' => $resName, 'country' => $resCountry, 'webrating' => $resWebRating, 'address' => $resAddress,
//                'price' => $resPrice);

            $allTypes = explode(',', $resFoodType);
            print_r($allTypes);
            echo "<div class='restaurant-listing'>
                    <div class='res-name'><a href='$resWebsite'>$resName</a></div>
                    <div class='res-country'>$resCountry</div>
                    <div class='res-webrating'>$resWebRating</div>
                    <div class='res-address'>$resAddress</div>
                    <div class='res-types'>
                    ";
            foreach ($allTypes as $singleType) {
                $singleType = ucwords($singleType);
                echo "<span class='tag label label-info'>$singleType</span>";
            }
            echo "</div>";

            if (strlen($resPrice) > 1) {
                echo "<div class='res-price'>$resPrice</div>";
            } else {
                echo "<div class='res-price invisible'>0</div>";
            }
            echo "</div>";
        }

    }

    // Close the database connection
    $conn->close();
}



retrieveResults($_POST["name"], isset($_POST["auto"]) ? $_POST["auto"] : 'no');