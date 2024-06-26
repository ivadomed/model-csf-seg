#Authors : William Sirois

# For usage, type: python fill-csf.py -h or in WSL python3 fill-csf.py -h
#J'importe ce dont j'ai besoin
import nibabel as nib
import cv2 as cv
from skimage.morphology import disk
from skimage.segmentation import flood_fill
import scipy as sc
import numpy as np
import argparse
def get_parser():
    parser = argparse.ArgumentParser(
    description="Close the segmentation of the CSF to get the segmentation of the canal." )
    parser.add_argument('-i', dest='CSF_seg', required = True, type=str,
                        help="Input segmentation of the CSF.")
    parser.add_argument('-o', dest='Output_name', required = True, type=str,
                        help="Ouput image name.")
    parser.add_argument('-s', dest='Cord_seg', required = True, type=str, 
                        help="Segmentation of the spinal cord ")

    return parser

def main() : 
    
    parser = get_parser()
    args = parser.parse_args()

#Fonction pour sauvegarder fournis par Sandrine
    def save_Nifti1(data, original_image, filename):
        empty_header = nib.Nifti1Header()
        image = nib.Nifti1Image(data, original_image.affine, empty_header)
        nib.save(image, filename)

#Je load l'image
    moelle = nib.load(args.Cord_seg)
    moelle_np = moelle.get_fdata()
    img = nib.load(args.CSF_seg)
    img_np = img.get_fdata()

#Je copie l'image pour avoir l'original pour la sauvegarder à la fin
    img_b = img_np.copy()
    moelle_b = moelle_np.copy()
#Image qui sera remplie (besoin pour éviter les floodfill quand ce n'est pas fermé)
    img_fill = img_b.copy()

#Méthode du floodfill avec le centre de masse
    imagenbr = img_b.shape[2]#Je prend le nombre de coupe transversale
    slice = 0
    h,w = img_b[:, :, 1].shape

    while slice < imagenbr : #J'itère sur les images de coupe
        if np.sum(img_b[:,:,slice] == 1) == 0 :#Si il n'y as pas de segmentation sur le csf on ne change rien
            img_fill[:, :, slice] = img_b[:, :, slice]

        elif np.sum(moelle_b[:,:,slice] == 1) == 0:#Si il n'y as pas de segmentation sur la moelle je ne change rien et je retire la segmentation du csf
            img_fill[:, :, slice] = 0
        
        else :
            cmmoelle = (sc.ndimage.center_of_mass(moelle_b[:, :, slice])) 
            cmmoelle = list(cmmoelle)
            cmmoelle[0] = int(cmmoelle[0])
            cmmoelle[1] = int(cmmoelle[1])
            img_fill[:,:,slice] = flood_fill(img_fill[:,:,slice], (cmmoelle[0],cmmoelle[1]), 1)

            if np.sum(img_fill[:,:,slice] == 1) == (h*w): #Si ma forme n'est pas fermée je reprend l'image de base et je fais une fermeture
                        img_fill[:, :, slice] = cv.morphologyEx(img_b[:,:,slice], cv.MORPH_CLOSE,disk(5))
            
        slice = slice+1 #Je passe à la prochaine slice

#Je sauvegarde l'image(Je ne sais pas comment renommer mes images seulement une façon qui ressemble à la votre)
    save_Nifti1(img_fill, img, args.Output_name)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main()
    print(f'Segmentation realised and saved in {args.Output_name}') 