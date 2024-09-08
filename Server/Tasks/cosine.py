
import numpy as np
import torch
import torchvision
from PIL import Image
from torch import nn
from torchvision import transforms as tr
from torchvision.models import vit_h_14, vit_b_16


class CosineSimilarity:
    """Class tasked with comparing similarity between two images """
    
    def __init__(self, image_path_2, device=None):

        if not device:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        self.image_path_1 = "template/0.jpeg"
        self.image_path_2 = image_path_2
    
    def model(self):
        """Instantiates the feature extracting model 
        
        Parameters
        ----------
        model
        Returns
        -------
        Vision Transformer model object
        """
        wt = torchvision.models.ViT_B_16_Weights.DEFAULT
        model = vit_b_16(weights=wt)
        model.heads = nn.Sequential(*list(model.heads.children())[:-1])
        model = model.to(self.device)

        return model

    def process_test_image(self, image_path):
        """Processing images
        Parameters
        ----------
        image_path :str
            
        Returns
        -------
        Processed image : str
        """
        if isinstance(image_path, str):
            img = Image.open(image_path)
        elif isinstance(image_path, np.ndarray):
            img = Image.fromarray(image_path)
        transformations = tr.Compose([tr.ToTensor(),
                                        tr.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                                        tr.Resize((224, 224))])
        img = transformations(img).float()
        img = img.unsqueeze_(0)
        
        img = img.to(self.device)

        return img

    def get_embeddings(self):
        """Computer embessings given images 
        
        Parameters
        image_paths : str
        Returns
        -------
        embeddings: np.ndarray
        """
        img1 = self.process_test_image(self.image_path_1)
        img2 = self.process_test_image(self.image_path_2)
        model = self.model()

        emb_one = model(img1).detach().cpu()
        emb_two = model(img2).detach().cpu()

        return emb_one, emb_two

    def compute_scores(self, x1=None, x2=None):
        """Computes cosine similarity between two vectors."""

        if not x1 and not x2:
            emb_one, emb_two = self.get_embeddings()
        elif x1 and x2:
            emb_one = (x1)
            emb_two = x2
        else:
            raise ValueError("Either both x1 and x2 should be provided or none of them should be provided.")
        
        scores = torch.nn.functional.cosine_similarity(emb_one, emb_two)

        return scores.numpy()