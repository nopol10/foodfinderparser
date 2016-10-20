<?php
/**
 * @param $name
 */
function displayResult($type)
{
    // Connect to database server
    $conn = new mysqli("localhost", "foodfinder", "foodfinder", "foodfinder");

    // Select database

    // Process food type
    $type = "%" . strtolower($type) . "%";
    // SQL query
    $strSQL = "SELECT restaurant_name, country, web_rating, address, average_price FROM restaurants WHERE food_type LIKE ? ORDER BY web_rating DESC 
               LIMIT 10";


    // Execute the query (the recordset $rs contains the result)
    if ($statement = $conn->prepare($strSQL)) {
        $statement->bind_param("s", $type);
        $statement->execute();
        $statement->bind_result($resName, $resCountry, $resWebRating, $resAddress, $resPrice);
        $i = 0;
        $outArray = array();
        while ($statement->fetch()) {
            $resCountry = ucfirst($resCountry);
            $resWebRating = $resWebRating * 100;
            $resPrice = '$' . $resPrice;
            $outArray[] = array('name' => $resName, 'country' => $resCountry, 'webrating' => $resWebRating, 'address' => $resAddress, 'price' => $resPrice);
            echo "<div class='restaurant-listing'>
                    <div class='res-name'>$resName</div>
                    <div class='res-country'>$resCountry</div>
                    <div class='res-webrating'>$resWebRating</div>
                    <div class='res-address'>$resAddress</div>
                    ";
            if (strlen($resPrice) > 1) {
                echo "<div class='res-price'>$resPrice</div>";
            } else {
                echo "<div class='res-price invisible'>0</div>";
            }
            echo "</div>";
        }
//        echo json_encode($outArray);
    }


    // Loop the recordset $rs
    // Each row will be made into an array ($row) using mysql_fetch_array
//    while ($row = mysql_fetch_array($rs)) {
//
//        // Write the value of the column FirstName (which is now in the array $row)
//        echo $row['FirstName'] . "<br />";
//    }
    $conn->close();
    // Close the database connection
}

displayResult($_POST["name"]);