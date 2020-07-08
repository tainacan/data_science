<?php
#Connecting to Wordpress
$_SERVER['SERVER_PROTOCOL'] = "HTTP/1.1";
$_SERVER['REQUEST_METHOD'] = "GET";

define( 'WP_USE_THEMES', false);
define( 'SHORTINIT', false);
require( '/var/www/html/wp-blog-header.php');

#Generating object instances for Collection, Metadata, Items, and Item_Metadata
$termsRepo = \Tainacan\Repositories\Terms::get_instance();
$taxonomyRepo = \Tainacan\Repositories\Taxonomies::get_instance();

#Getting the Taxonomy
$taxonomy = $taxonomyRepo->fetch(['name' => 'Classificação 2'], 'OBJECT');
$taxonomy = $taxonomy[0];



$terms = $termsRepo->fetch(['posts_per_page' => -1],$taxonomy);

$file = fopen('classificacao2.csv', 'w');
	
	fputcsv($file, ["Classificação 2"]);
	
	foreach($terms as $term){
	
		#echo "Processando item {$term->get_name()}\n\n";
	
		$term_name = str_replace(" people","",$term);
		$term_name = str_replace("Hello, my name is ","",$term_name);
		
		echo $term_name;
		echo "\n";
		
		fputcsv($file, [$term_name]);
				
		
		/*
		$term->set_name($term_name);
	
		if ($term->validate()){
			$termsRepo->insert($term);
			echo "Salvando termo setado\n";
		
		}else{
			echo 'Item não validado: ', $term->get_name();
		}
		*/
}
fclose($file);


?>
