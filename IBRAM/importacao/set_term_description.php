<?php
#Connecting to Wordpress
$_SERVER['SERVER_PROTOCOL'] = "HTTP/1.1";
$_SERVER['REQUEST_METHOD'] = "GET";

define( 'WP_USE_THEMES', false );
define( 'SHORTINIT', false );
require( '/var/www/html/wp-blog-header.php' );

#Generating object instances for Collection, Metadata, Items, and Item_Metadata
$metadataRepo = \Tainacan\Repositories\Metadata::get_instance();
$termsRepo = \Tainacan\Repositories\Terms::get_instance();
$taxonomyRepo = \Tainacan\Repositories\Taxonomies::get_instance();


$taxonomy = $taxonomyRepo->fetch(['name' => 'Classificação 2'], 'OBJECT');
$taxonomy = $taxonomy[0];

$terms = $termsRepo->fetch(['posts_per_page' => -1],$taxonomy);

#Csv file with terms description
$file = fopen('classificacao2.csv', 'r');

while (($data = fgetcsv($file, 0, ",")) == TRUE){
	
	foreach($terms as $term){
		
		$term_name = str_replace(" people","",$term);
		$term_name = str_replace("Hello, my name is ","",$term_name);
		
		if ($term_name == $data[0]){
		
			$term->set_description($data[1]);

			if ($term->validate()){

				$termsRepo->insert($term);

				echo "Salvando termo setado\n";
			}else{
				echo 'Item não validado', $term->get_name();
			}
		}
	}
}

fclose($file);

?>
