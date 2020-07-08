
<?php

#Connecting to Wordpress
$_SERVER['SERVER_PROTOCOL'] = "HTTP/1.1";
$_SERVER['REQUEST_METHOD'] = "GET";

define( 'WP_USE_THEMES', false );
define( 'SHORTINIT', false );
require( '**/wp-blog-header.php' );

#Generating object instances for Collection, Metadata, Items, and Item_Metadata
$collectionsRepo = \Tainacan\Repositories\Collections::get_instance();
$metadataRepo = \Tainacan\Repositories\Metadata::get_instance();
$itemsRepo = \Tainacan\Repositories\Items::get_instance();
$itemMetadataRepo = \Tainacan\Repositories\Item_Metadata::get_instance();

#################################

#Setting relational collections
$pessoas_collection = $collectionsRepo->fetch(['name'=>'**'], 'OBJECT');
$pessoas_collection = $pessoas_collection[0];

$entidades_collection = $collectionsRepo->fetch(['name'=>'**'], 'OBJECT');
$entidades_collection = $entidades_collection[0];

#Array Itens de Pessoa
$itens_pessoas = $itemsRepo->fetch(['title'=>'', 'posts_per_page'=> '-1'],$pessoas_collection, 'OBJECT');

foreach ($itens_pessoas as $item_pessoa){
	
	$itemMetadataPessoa = $itemMetadataRepo->fetch($item_pessoa,$metadata[0], ['title'=>'**']);
	
	$array_pessoas [$itemMetadataPessoa[0]->get_value()] = $item_pessoa;
}

#Array Itens de Entidade
$itens_entidades = $itemsRepo->fetch(['title'=>'', 'posts_per_page'=> '-1'],$entidades_collection, 'OBJECT');

foreach ($itens_entidades as $item_entidade){
	
	$itemMetadataEntidade = $itemMetadataRepo->fetch($item_entidade,$metadata[0], ['title'=>'**']);
	
	$array_entidades [$itemMetadataEntidade[0]->get_value()] = $item_entidade;
}

#################################

#Getting the Colletion
$collection = $collectionsRepo->fetch(['name'=>'**'], 'OBJECT');
$collection = $collection[0];


$fh = fopen("itens_documentos.csv", "r") or die("ERROR OPENING DATA");

while (($data = fgetcsv($fh, 0, ",")) == TRUE){
	$linecount++;
}
fclose($fh);


#Getting metadata title from csv array

if (($handle = fopen("itens_documentos.csv", "r")) == TRUE) {
	
	$cont = 0;
	
	while (($data = fgetcsv($handle, 0, ",")) == TRUE){
		
		if($cont == 0){
			
			echo "Tratando primeira linha \n";
			$headers = array_map('trim', $data);
			
		}else{
			
			$item = new \Tainacan\Entities\Item();
			
			$item->set_title($data[0]);
			$item->set_status('publish');
			$item->set_collection($collection);
			
			if ($item->validate()) {
				
				$item = $itemsRepo->insert($item);
				for ($i = 0; $i <=sizeof($data); $i++) {
					
					$metadatum = $metadataRepo->fetch(['name' => $headers[$i]], 'OBJECT');
					$metadatum = $metadatum[0];
					
					
					if ($metadatum->get_metadata_type() == 'Tainacan\Metadata_Types\Taxonomy'){
						
						$itemMetadata = new \Tainacan\Entities\Item_Metadata_Entity($item, $metadatum);
						$taxonomy_value = explode("||",$data[$i]);
						$itemMetadata->set_value($taxonomy_value);
						
					} else if ($metadatum->get_metadata_type() == 'Tainacan\Metadata_Types\Relationship'){
						
						$itemMetadata = new \Tainacan\Entities\Item_Metadata_Entity($item, $metadatum);
						$relationship_value = explode("||",$data[$i]);
						$relationship_array = [];
						
						if (strpos($metadatum->get_name(), 'Pessoa')!== false){
							foreach($relationship_value as $item_id){
								if ($array_pessoas[$item_id] != Null){
									echo $array_pessoas[$item_id]->get_id();
									echo "\n";
									$relationship_array [] = $array_pessoas[$item_id]->get_id();
								}
								else{
									$relationship_array [] = $array_pessoas[]->get_id();
								}
							}
						}
						else if (strpos($metadatum->get_name(), 'Entidade')!== false){
							foreach($relationship_value as $item_id){
								if ($array_entidades[$item_id] != Null){
									$relationship_array [] = $array_entidades[$item_id]->get_id();
								}
								else{
									$relationship_array [] = $array_entidades[]->get_id();
								}
							}
						}
						
						$itemMetadata->set_value($relationship_array);
					
					}else{
						
						$itemMetadata = new \Tainacan\Entities\Item_Metadata_Entity($item, $metadatum);
						$metadata_text = explode("||",$data[$i])
						$itemMetadata->set_value($metadata_text);
					}
					
					if ($itemMetadata->validate()) {
						
						$itemMetadataRepo->insert($itemMetadata);
						
					}else {
						echo 'Erro no metadado ', $metadatum->get_name(), ' no item ', $data[0];
						$erro = $itemMetadata->get_errors();
						echo var_dump($erro);
					}
				}
				if ($item->validate()) {
					$item = $itemsRepo->insert($item);
					echo 'Item ', $data[0], ' - inserted', "\n";
					echo $linecount-$cont, ' remain', "\n";
					echo ($cont/$linecount)*100, '% Completed', "\n" ,"\n";
				}else{
					echo 'Erro no preenchientos dos campos', $cont, "\n";
					$errors = $item->get_errors();
					var_dump($errors);
					echo  "\n\n";
					die;
				}
				
			}else {
				echo 'Erro na linha ', $cont;
				echo  "\n\n";
				var_dump($item);
				echo  "\n\n";
				die;
			}
			
		}
		$cont+=1;
	}
fclose($handle);
}


?>

