<html>
<body>

<?php
$servername = "127.0.0.1";
$username = "root";
$password = "128bitslonger";
$db = "application";
$port = "3306";

// Create connection
$conn = new mysqli($servername, $username, $password, $db, $port);

if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
} 
else {
  echo '<table border = "1" cellspacing = "2" cellpadding = "2">
        <tr>
            <th>Name</th>
            <th>Latitude</th>
            <th>Longitude</th>
        </tr>';

  $query = "SELECT * from application.waypoints";

  if ($result = $conn->query($query)) {
    while ($row = $result->fetch_assoc()) {
      $waypoints = $row["Name"];
      $latitude = $row["Latitude"];
      $longtitude = $row["Longitude"];

      echo '<tr>
                 <td>'.$waypoints.'</td>
                 <td>'.$latitude.'</td>
                 <td>'.$longtitude.'</td>
            </tr>';
    }
    $result->free();
  }
}
?>

</body>
</html>
