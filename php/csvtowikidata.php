<?php
require_once( __DIR__ . "/vendor/autoload.php" );

use DataValues\NumberValue;

function fetch_file($url, $path)
{
    $opts = array('http' => array('header' => "User-Agent:MyAgent/1.0\r\n"));
    $context = stream_context_create($opts);
    $content = file_get_contents($url, FALSE, $context);
    file_put_contents($path, $content);
    return $path;
}

function csv_to_array($filename='', $delimiter=',')
{
    if(!file_exists($filename) || !is_readable($filename))
        return FALSE;

    $header = null;
    $data = array();
    if (($handle = fopen($filename, 'r')) !== FALSE) {
        while (($row = fgetcsv($handle, 1000, $delimiter)) !== FALSE) {
            if(!$header) {
                $header = array_map('strtolower', $row);
            } else {
                $data[] = array_combine($header, $row);
            }
        }
        fclose($handle);
    }
    return $data;
}

$zurich_districts = array(
    '111' => "Q382903",
    '91' => "Q80797",
    '92' => "Q445711",
    '31' => "Q433012",
    '14' => "Q1093831",
    '24' => "Q648218",
    '52' => "Q687052",
    '71' => "Q693269",
    '33' => "Q693357",
    '51' => "Q693413",
    '44' => "Q870084",
    '73' => "Q476940",
    '123' => "Q693374",
    '12' => "Q39240",
    '101' => "Q455496",
    '72' => "Q693454",
    '42' => "Q1805410",
    '23' => "Q691367",
    '13' => "Q10987378",
    '82' => "Q693397",
    '63' => "Q693483",
    '115' => "Q167179",
    '11' => "Q692511",
    '121' => "Q652455",
    '122' => "Q657525",
    '119' => "Q276792",
    '81' => "Q692773",
    '34' => "Q370104",
    '61' => "Q656446",
    '83' => "Q693321",
    '41' => "Q531899",
    '102' => "Q678030",
    '74' => "Q392079",
    '21' => "Q642353",
);

$filename = "zurich_population.csv";
$download_url = "http://data.stadt-zuerich.ch/content/portal/de/index/ogd/daten/bevoelkerungsbestand_jahr_quartier_seit1970/jcr:content/data/ogdfile/file.res/bevoelkerungsbestand_jahr_quartier_seit1970.csv";

$path = fetch_file($download_url, $filename);
$data = csv_to_array($path);

// Set stuff up and login
$api = new \Mediawiki\Api\MediawikiApi("http://www.wikidata.org/w/api.php");
$api->login(new \Mediawiki\Api\ApiUser('Csvtodata', 'hackathon2014'));
$services = new \Wikibase\Api\ServiceFactory($api);
$repo = $services->newRevisionRepo();
$saver = $services->newRevisionSaver();


// update the wikidata items
foreach ($data as $districtData) {
    $item_id = $zurich_districts[$districtData['qnr']];
    $population2013 = $districtData['wbev_2013'];

    $propertyId = 1082; // id of population property
    $dataValue = new NumberValue((int)$population2013);
    $propertyValue = new \Wikibase\DataModel\Snak\PropertyValueSnak($propertyId, $dataValue);
    $claim = new \Wikibase\DataModel\Claim\Claim($propertyValue);

    $entity = $repo->getEntityResultById($item_id);
    $entity->addClaim($claim);
}
