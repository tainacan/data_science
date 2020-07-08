#OBS. ALTERAR A EXIBIÇÃO DOS METADADOS PARA NUNCA MOSTRAR.

<?php
#Connecting with Wordpress:
$_SERVER['SERVER_PROTOCOL'] = "HTTP/1.1";
$_SERVER['REQUEST_METHOD'] = "GET";
        
define( 'WP_USE_THEMES', false );
define( 'SHORTINIT', false );

#Path of wp
require( '*..wp-blog-header.php');

$collectionsRepo = \Tainacan\Repositories\Collections::get_instance();
$metadataRepo = \Tainacan\Repositories\Metadata::get_instance();
$taxonomyRepo = \Tainacan\Repositories\Taxonomies::get_instance();

#Setting relational collections
$pessoas_collection = $collectionsRepo->fetch(['name'=>'**'], 'OBJECT');
$pessoas_collection = $pessoas_collection[0];

$pessoas_id = $metadataRepo->fetch(['name'=>'**', 'collection_id'=>$pessoas_collection->get_id()], 'OBJECT');
$pessoas_id = $pessoas_id[0];

$entidades_collection = $collectionsRepo->fetch(['name'=>'**'], 'OBJECT');
$entidades_collection = $entidades_collection[0];

$entidades_id = $metadataRepo->fetch(['name'=>'**', 'collection_id'=>$entidades_collection->get_id()], 'OBJECT');
$entidades_id = $entidades_id[0];

#Delete Existing Collections:
/*
$collections = $collectionsRepo->fetch([], 'OBJECT');
foreach ($collections as $col) {
	echo "Deleting collection ", $col->get_id(), "\n";
	$collectionsRepo->delete([$col->get_id(), true]);
}
*/

#Create Collection and Metadata:
$collection = new \Tainacan\Entities\Collection();
$collection->set_name('**');
$collection->set_status('publish');
$collection->set_description('**');

$cont = 0;
if ($collection->validate()) {
	$insertedCollection = $collectionsRepo->insert($collection);

	if (($handle = fopen("tables_import/metadata_museu.csv", "r")) == TRUE) {
		
		$collection_core_metadata = $metadataRepo->get_core_metadata($insertedCollection);
		
		while (($data = fgetcsv($handle, 0, ",")) == TRUE){
			if ($cont == 0){
				echo "Pulando linha das colunas", "\n";
			} else{
				if (trim($data[3]) == 'Description' OR trim($data[3]) == 'Title'){
					foreach ($collection_core_metadata as $coreMetadata) {
						if($coreMetadata->get_name() == $data[3]){
							$coreMetadata->set_name($data[0]);
							$coreMetadata->set_description($data[1]);
							echo "Atualizando Core Field: ", $data[0], "\n";
						
							if ($coreMetadata->validate()){
								$insertedMetadata = $metadataRepo->insert($coreMetadata);
							} else {
								$erro = $coreMetadata->get_errors();
								var_dump($erro);
							}
						}
					}
				} else {
					
					if (trim($data[2]) == 'Tainacan\Metadata_Types\Taxonomy'){
						
						$taxonomy = new \Tainacan\Entities\Taxonomy;
						$taxonomy->set_name(trim($data[0]));
						$taxonomy->set_description("Taxonomia para o metadado ". trim($data[0]));
						$taxonomy->set_allow_insert('yes');
						$taxonomy->set_status('publish');
						
						if ($taxonomy->validate()) {
							$insertedTaxonomy = $taxonomyRepo->insert($taxonomy);
							echo 'Taxonomy created with ID -  ' . $taxonomy->get_id(), "\n";
							
						} else {
								$error = $taxonomy->get_errors();
								var_dump($error);
						}
						
						$metadata_type_options = ['taxonomy_id' => $insertedTaxonomy->get_id(), 
						'input_type' => 'tainacan-taxonomy-tag-input', 'allow_new_terms' => 'yes', 'multiple'=>'yes'];
						
						$metadado = new \Tainacan\Entities\Metadatum();
						$metadado->set_collection($insertedCollection);
						$metadado->set_name(trim($data[0]));
						$metadado->set_description($data[1]);
						$metadado->set_metadata_type(trim($data[2]));
						$metadado->set_multiple('yes');
						$metadado->set_status('publish');
						$metadado->set_display('no');
						$metadado->set_metadata_type_options($metadata_type_options);
						
					}else if (trim($data[2]) == 'Tainacan\Metadata_Types\Relationship'){
					
						echo "\n","Metadado Relacionamento", "\n";
						
						if (trim($data[3]) == 'Entidade'){
						
							echo "\n","Metadado Relacionamento ENTIDADES", "\n";

							$metadata_type_options = ['collection_id' => $entidades_collection->get_id(), 
							'multiple'=>'yes', 'repeated'=>'yes', 'input_type' => 'tainacan-taxonomy-tag-input', 
							'search'=>(string)$entidades_id->get_id()];
							
							$metadado = new \Tainacan\Entities\Metadatum();
							$metadado->set_collection($insertedCollection);
							$metadado->set_name(trim($data[0]));
							$metadado->set_description($data[1]);
							$metadado->set_metadata_type(trim($data[2]));
							$metadado->set_multiple('yes');
							$metadado->set_status('publish');
							$metadado->set_display('no');
							$metadado->set_metadata_type_options($metadata_type_options);
							
						}else if (trim($data[3]) == 'Pessoa'){
						
							echo "\n","Metadado Relacionamento PESSOAS", "\n";
				
							$metadata_type_options = ['collection_id' => $pessoas_collection->get_id(), 'multiple'=>'yes', 
							'repeated'=>'yes', 'input_type' => 'tainacan-taxonomy-tag-input', 'search'=>(string)$pessoas_id->get_id()];
							
							$metadado = new \Tainacan\Entities\Metadatum();
							$metadado->set_collection($insertedCollection);
							$metadado->set_name(trim($data[0]));
							$metadado->set_description($data[1]);
							$metadado->set_metadata_type(trim($data[2]));
							$metadado->set_multiple('yes');
							$metadado->set_status('publish');
							$metadado->set_display('no');
							$metadado->set_metadata_type_options($metadata_type_options);
						}
						
						}else if (trim($data[4]) == 'X'){
						
							echo "\n","Metadado de Texto Multivalorado", "\n";
				
							$metadata_type_options = ['multiple'=>'yes', 'repeated'=>'yes', 
							'input_type' => 'tainacan-taxonomy-tag-input'];
							
							$metadado = new \Tainacan\Entities\Metadatum();
							$metadado->set_collection($insertedCollection);
							$metadado->set_name(trim($data[0]));
							$metadado->set_description($data[1]);
							$metadado->set_metadata_type(trim($data[2]));
							$metadado->set_status('publish');
							$metadado->set_display('no');
							$metadado->set_metadata_type_options($metadata_type_options);
						}
					
					}else{
					
						$metadado = new \Tainacan\Entities\Metadatum();
						$metadado->set_collection($insertedCollection);
						$metadado->set_name(trim($data[0]));
						$metadado->set_description($data[1]);
						$metadado->set_metadata_type(trim($data[2]));
						$metadado->set_status('publish');
						$metadado->set_display('no');
					}
				
					if ($metadado->validate()){
						$insertedMetadata = $metadataRepo->insert($metadado);
					} else {
						$erro = $metadado->get_errors();
						var_dump($erro);
					}
				
				}
			}
			
		$cont+=1;
		
		}
		
	fclose($handle);
	
	}
	
	if ($insertedCollection->validate()) {
		$insertedCollection = $collectionsRepo->insert($insertedCollection);
		echo 'Collection created with ID -  ' . $insertedCollection->get_id(), "\n";
	} else {
		$errors = $insertedCollection->get_errors();
	}
	
}else {
	$validationErrors = $collection->get_errors();
	echo $validationErrors;
	die;
}
?>


