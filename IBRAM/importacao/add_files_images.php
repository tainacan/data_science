
<?php
#Connecting to Wordpress
$_SERVER['SERVER_PROTOCOL'] = "HTTP/1.1";
$_SERVER['REQUEST_METHOD'] = "GET";
        
define( 'WP_USE_THEMES', false );
define( 'SHORTINIT', false );
require( '*..\wp-blog-header.php' );

$metadataRepo = \Tainacan\Repositories\Metadata::get_instance();
$itemsRepo = \Tainacan\Repositories\Items::get_instance();
$itemMedia = \Tainacan\Media::get_instance();

#DEFINIR O VALOR DO CAMPO COM O THUMBNAIL
$metadataImages = $metadataRepo->fetch(['name'=>''], 'OBJECT');
$metadataImages = $metadataImages[0];


$meta_query = [
	[
		'key' => $metadataImages->get_id(),
		'value' => '',
		'compare' => 'NOT IN'
	]
];

$items = $itemsRepo->fetch(['meta_query' => $meta_query, 'posts_per_page' => -1], 
$metadataImages->get_collection(), 'OBJECT');


$conta_item = 1;
$items_size = sizeof($items);

foreach ($items as $item) {
	
	$metaDocument = new \Tainacan\Entities\Item_Metadata_Entity($item, $metadataImages);
	
	echo "Processando item {$item->get_title()}\n\n";
	
	$imgs_array = explode("||",$metaDocument->get_value());
	
	$imgs_array_size = sizeof($imgs_array);
	
	$conta = 0;
	foreach($imgs_array as $img){
		
		if ($conta == 0){
			$idMedia = $itemMedia->insert_attachment_from_file("Imagens/".$img);
			echo "Adicionando documento: $img \n";
			
			if (false != $idMedia){
				
				$item->set_document($idMedia);
				$item->set_document_type('attachment');
				$item->set__thumbnail_id($idMedia);
		
				if ($item->validate()){
					
					$itemsRepo->insert($item);
					echo "Salvando item com documento setado\n";
					
				} else{
					
					echo 'Item não validado: ', $item->get_title();
				} 
		
			} else {
				
				echo 'Erro ao adicionar a media ', $metaDocument->get_value(), "\n\n";
			}
		} else if($imgs_array_size > 1){
			
			$itemMedia->insert_attachment_from_file("Imagens/".$img, $item->get_id());
			echo "Adicionando anexo: $img \n";
		
		}
		
		$conta+=1;
		
	}
	
	echo "Remain ", $items_size-$conta_item;
	echo "\n\n";
	$conta_item+=1;	
	
}
?>
