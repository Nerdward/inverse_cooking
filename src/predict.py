import pickle
import torch
from src.model import get_model
from src.args import get_parser
from PIL import Image
from io import BytesIO
from torchvision import transforms
from src.utils.output_utils import prepare_output


greedy = [True, False, False, False]
beam = [-1, -1, -1, -1]
temperature = 1.0
numgens = len(greedy)
use_gpu = False
device = torch.device('cuda' if torch.cuda.is_available() and use_gpu else 'cpu')
map_loc = None if torch.cuda.is_available() and use_gpu else 'cpu'
show_anyways = False

def load_image(image_file):
    image = Image.open(BytesIO(image_file))
    return image

def preprocess(image):
    transf_list_batch = []
    transf_list_batch.append(transforms.ToTensor())
    transf_list_batch.append(transforms.Normalize((0.485, 0.456, 0.406), 
                                                (0.229, 0.224, 0.225)))
    to_input_transf = transforms.Compose(transf_list_batch)
    transf_list = []
    transf_list.append(transforms.Resize(256))
    transf_list.append(transforms.CenterCrop(224))
    transform = transforms.Compose(transf_list)
    
    image_transf = transform(image)
    image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)

    return image_tensor

def load_artifacts(ingr_path, vocab_path, model_path):
    import sys; sys.argv=['']; del sys
    args = get_parser()
    args.maxseqlen = 15
    args.ingrs_only=False
    ingrs_vocab = pickle.load(open(ingr_path, 'rb'))
    vocab = pickle.load(open(vocab_path, 'rb'))

    ingr_vocab_size = len(ingrs_vocab)
    instrs_vocab_size = len(vocab)
    model = get_model(args, ingr_vocab_size, instrs_vocab_size)
    # Load the trained model parameters

    model.load_state_dict(torch.load(model_path, map_location=map_loc))

    return model, ingrs_vocab, vocab

def predict(model, ingrs_vocab, vocab, image_tensor):
    model.to(device)
    model.eval()
    model.ingrs_only = False
    model.recipe_only = False
    num_valid = 0
    recipes = {}
    for i in range(numgens):
        with torch.no_grad():
            outputs = model.sample(image_tensor, greedy=greedy[i], 
                                temperature=temperature, beam=beam[i], true_ingrs=None)
            
        ingr_ids = outputs['ingr_ids'].cpu().numpy()
        recipe_ids = outputs['recipe_ids'].cpu().numpy()
            
        outs, valid = prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)
        
        if valid['is_valid'] or show_anyways:
            num_valid+=1
            BOLD = '\033[1m'
            END = '\033[0m'
            recipe_number = f"RECIPE {num_valid}"
            title = f"""
                    {outs['title']}
                    """  
            ingredients = """
                        INGREDIENTS:
                        """ + ",".join(outs['ingrs'])
            instructions = '-'+'\n-'.join(outs['recipe'])
            
            # return recipe_number + title + ingredients + instructions
            return {
                        "RECIPE": num_valid,
                        "TITLE": f"{outs['title']}",
                        "INGREDIENTS": ",".join(outs['ingrs']),
                        "INSTRUCTIONS": '-'+'\n-'.join(outs['recipe'])
                    }
                                    

#             recipes[num_valid] = {
#                                     "RECIPE": num_valid,
#                                     "TITLE": f"{outs['title']}",
#                                     "INGREDIENTS": ",".join(outs['ingrs']),
#                                     "INSTRUCTIONS": '-'+'\n-'.join(outs['recipe'])
#                                 }
            
            # print ('RECIPE', num_valid)
            # num_valid+=1
            # #print ("greedy:", greedy[i], "beam:", beam[i])
    
            # BOLD = '\033[1m'
            # END = '\033[0m'
            # print (BOLD + '\nTitle:' + END,outs['title'])

            # print (BOLD + '\nIngredients:'+ END)
            # print (', '.join(outs['ingrs']))

            # print (BOLD + '\nInstructions:'+END)
            # print ('-'+'\n-'.join(outs['recipe']))

            # print ('='*20)
        else:
            pass
            print ("Not a valid recipe!")
            print ("Reason: ", valid['reason'])
        # return recipe_number + title + ingredients + instructions
