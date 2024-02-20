**Installation**
Pour utiliser le code de segmentation du canal spinal à partir des segmentations de la moelle et du CSF il est nécessaire d'installer les librairies utilisées. la ligne qui permet d'installer ces librairie est incluse dans celles pour cloner le Github.
Ensuite, il faut cloner le Github à l'aide de la suite de commande suivante : 


**Fonctionnement**
À partir de la segmentation de la moelle, le centre de masse est déterminé pour chaque tranche transversale.
Si il n'y as pas de segmentation du CSF (le CSF n'apparait pas sur l'image), on ne remplace pas l'image.
Si il n'y as pas de segmentation de la moelle, on met l'image à 0.
Si le CSF et la moelle on des segmentations sur la tranche, un floodfill est fait à partir du centre de masse déterminé plus haut.
Le code évalue ensuite si l'image est pleine de 1 (région non fermée lors du floodfill)
Si l'image est pleine de 1, on reprend l'image de base et on fait une fermeture.
Le fait de faire la fermeture sur certaines images ne semble pas causée d'ajout de bruit à l'extérieur du CSF selon ce que j'ai observé.

**Utilisation**
Le code prend en entrée 3 arguments   

-s Le fichier nii.gz de segmentation de la moelle épinière  

-o Le nom que vous souhaiter donner au fichier  

-i Le fichier nii.gz de la segmentation du csf  
