from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle
import gradio as gr
svc=pickle.load(open('svc.pickle','rb'))
def predict_class(cap_shape, cap_surface, cap_color, bruises, odor, gill_attachment, 
                  gill_spacing, gill_size, gill_color, stalk_shape, stalk_root, 
                  stalk_surface_above_ring, stalk_surface_below_ring, stalk_color_above_ring, 
                  stalk_color_below_ring, veil_color, ring_number, ring_type, spore_print_color, 
                  population, habitat):
    input_data=[cap_shape, cap_surface, cap_color, bruises, odor, gill_attachment, 
                  gill_spacing, gill_size, gill_color, stalk_shape, stalk_root, 
                  stalk_surface_above_ring, stalk_surface_below_ring, stalk_color_above_ring, 
                  stalk_color_below_ring, veil_color, ring_number, ring_type, spore_print_color, 
                  population, habitat]
    encoder=LabelEncoder()
    real_df=pd.read_csv('mushrooms.csv')
    real_df.drop(['class','veil-type'],axis=1,inplace=True)
    encoded_value=[]
    features = [ 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
           'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
           'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
           'stalk-surface-below-ring', 'stalk-color-above-ring',
           'stalk-color-below-ring', 'veil-color', 'ring-number',
           'ring-type', 'spore-print-color', 'population', 'habitat']
    randomly_selected_values = ['s', 'y', 'g', 'f', 'c', 'a', 'w', 'n', 'b', 't', 'e', 's', 'k', 'o', 'y', 'w', 'o', 'f', 'r', 'y', 'p']
    random=pd.DataFrame([input_data],columns=features)
    for i in real_df.columns:
        encoder.fit_transform(real_df[i])
        encoded_value.append(encoder.transform(random[i])[0])
    
    prediction=svc.predict([encoded_value])
    class_label = 'poisonous' if prediction == 1 else 'edible'
    return class_label







import gradio as gr
input_features = {
    'cap-shape': ['x', 'b', 's', 'f', 'k', 'c'],
    'cap-surface': ['s', 'y', 'f', 'g'],
    'cap-color': ['n', 'y', 'w', 'g', 'e', 'p', 'b', 'u', 'c', 'r'],
    'bruises': ['t', 'f'],
    'odor': ['p', 'a', 'l', 'n', 'f', 'c', 'y', 's', 'm'],
    'gill-attachment': ['f', 'a'],
    'gill-spacing': ['c', 'w'],
    'gill-size': ['n', 'b'],
    'gill-color': ['k', 'n', 'g', 'p', 'w', 'h', 'u', 'e', 'b', 'r', 'y', 'o'],
    'stalk-shape': ['e', 't'],
    'stalk-root': ['e', 'c', 'b', 'r', '?'],
    'stalk-surface-above-ring': ['s', 'f', 'k', 'y'],
    'stalk-surface-below-ring': ['s', 'f', 'y', 'k'],
    'stalk-color-above-ring': ['w', 'g', 'p', 'n', 'b', 'e', 'o', 'c', 'y'],
    'stalk-color-below-ring': ['w', 'p', 'g', 'b', 'n', 'e', 'y', 'o', 'c'],
    'veil-color': ['w', 'n', 'o', 'y'],
    'ring-number': ['o', 't', 'n'],
    'ring-type': ['p', 'e', 'l', 'f', 'n'],
    'spore-print-color': ['k', 'n', 'u', 'h', 'w', 'r', 'o', 'y', 'b'],
    'population': ['s', 'n', 'a', 'v', 'y', 'c'],
    'habitat': ['u', 'g', 'm', 'd', 'p', 'w', 'l']
}


# Convert input features dictionary to a list of dictionaries
print(len(input_features))
# Define the output classes
output_classes = ['p', 'e']

input_components = [gr.Dropdown(choices=values, label=feature) for feature, values in input_features.items()]

# Create Gradio interface
iface = gr.Interface(
    fn=predict_class,
    inputs=input_components,
    outputs="label",
    title="Mushroom Classifier",
    description="Predict whether a mushroom is poisonous or edible based on its features."
)
iface.launch(inline=False,share=True)
