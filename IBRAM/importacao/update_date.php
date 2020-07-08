<?php

#Connecting to Wordpress
$_SERVER['SERVER_PROTOCOL'] = "HTTP/1.1";
$_SERVER['REQUEST_METHOD'] = "GET";

define( 'WP_USE_THEMES', false );
define( 'SHORTINIT', false );
require( 'C:\wamp\www\wordpress\wp-blog-header.php' );

#Generating object instances for Collection, Metadata, Items, and Item_Metadata
$collectionsRepo = \Tainacan\Repositories\Collections::get_instance();
$metadataRepo = \Tainacan\Repositories\Metadata::get_instance();
$itemsRepo = \Tainacan\Repositories\Items::get_instance();
$itemMetadataRepo = \Tainacan\Repositories\Item_Metadata::get_instance();
$taxRepo = \Tainacan\Repositories\Taxonomies::get_instance();

#Getting the Colletion
$collection = $collectionsRepo->fetch_one(['name'=>'Museu do Índio']);
$tax = $taxRepo->fetch_one(['name' => 'Possui fotografia']);

$term = get_term_by('slug', 'sim', $tax->get_db_identifier() );

$term_id = $term->term_taxonomy_id;

global $wpdb;

$query = "UPDATE $wpdb->posts SET post_date = DATE_ADD(post_date, INTERVAL 1 DAY),
	post_date_gmt = DATE_ADD(post_date_gmt, INTERVAL 2 DAY)
	WHERE ID IN (
		SELECT object_id FROM $wpdb->term_relationships WHERE 
			term_taxonomy_id = $term_id 
	) 
";

var_dump($query);

$run = $wpdb->query($query);

var_dump($run);
