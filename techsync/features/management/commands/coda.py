import os
import google.generativeai as genai
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Interacts with Google Gemini API to provide responses based on user input'

    def handle(self, *args, **kwargs):
        # Load environment variables
        load_dotenv()

        # Configure the API key for Gemini
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        # Create the model
        generation_config = {
          "temperature": 1,
          "top_p": 0.95,
          "top_k": 64,
          "max_output_tokens": 8192,
          "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
          model_name="gemini-1.5-pro",
          generation_config=generation_config,
          # safety_settings = Adjust safety settings if needed
        )

        # Start a chat session
        chat_session = model.start_chat(
          history=[
            {
              "role": "user",
              "parts": [
                "hey\n",
              ],
            },
            {
              "role": "model",
              "parts": [
                "Hey there! 👋 Welcome to Techsync, Ethiopia's developer community. I'm Coda, your friendly virtual assistant. How can I help you today? 😊 \n",
              ],
            },
            {
              "role": "user",
              "parts": [
                "give me an idea on computer science final project",
              ],
            },
            {
              "role": "model",
              "parts": [
                "Hey there! I'd love to help you brainstorm some computer science final project ideas. To give you the most relevant suggestions, could you tell me a bit more about your preferences? \n\nFor example, what are you most interested in within computer science? \n\n* **Specific areas:** Do you love algorithms, machine learning, web development, game development, cybersecurity, etc.?\n* **Level of complexity:** Are you looking for something simple or more challenging? \n* **Available resources:** Do you have access to specific hardware or software? \n* **Personal interests:** Do you enjoy working on projects related to a particular hobby or field, like music, art, or social impact? \n\nThe more details you can provide, the better I can suggest ideas that will be both interesting and achievable for you. 😊 \n",
              ],
            },
            {
              "role": "user",
              "parts": [
                "in machine learning",
              ],
            },
            {
              "role": "model",
              "parts": [
                "That's great! Machine learning is a fascinating and growing field. Here are some project ideas that span different levels of complexity, and you can choose one that fits your skills and resources:\n\n**Beginner Level:**\n\n* **Image Classification:** Build a system that can classify images into different categories, like animals, objects, or emotions. You can use a pre-trained model like ResNet or VGG and fine-tune it for your specific dataset.\n* **Sentiment Analysis:** Create a program that analyzes text data (e.g., movie reviews, social media posts) to determine the overall sentiment (positive, negative, or neutral). You can use libraries like NLTK or spaCy for text processing and a classification algorithm like Naive Bayes.\n* **Predictive Modeling:** Develop a model that predicts future values based on historical data. For example, you could build a model that predicts stock prices or weather patterns. You can use libraries like scikit-learn for model building and evaluation.\n\n**Intermediate Level:**\n\n* **Recommendation System:** Create a personalized recommendation system that suggests products, movies, or music based on user preferences. You can use collaborative filtering or content-based filtering techniques.\n* **Anomaly Detection:** Build a system that identifies unusual patterns or outliers in data. This could be useful for detecting fraudulent transactions, network intrusion attempts, or machine failures.\n* **Time Series Analysis:** Develop a model that analyzes and forecasts data over time. You could apply this to predict sales trends, stock market movements, or traffic patterns.\n\n**Advanced Level:**\n\n* **Natural Language Processing (NLP) Task:** Explore a complex NLP task like machine translation, text summarization, question answering, or chatbot development.\n* **Reinforcement Learning:** Develop an agent that learns to perform tasks through trial and error. You could create a game-playing agent, a robot navigation system, or a control system for a physical system.\n* **Computer Vision:** Work on a computer vision project like object detection, image segmentation, or facial recognition. You can use libraries like OpenCV and TensorFlow.\n\n**Important Considerations:**\n\n* **Dataset:** Choose a dataset that's relevant to your project and that you have access to. Many open-source datasets are available online.\n* **Algorithms:** Research and choose suitable machine learning algorithms for your task. Consider the data characteristics and the desired outcome.\n* **Evaluation Metrics:** Select appropriate metrics to evaluate the performance of your model.\n* **Documentation:** Document your project thoroughly, including the dataset, algorithms, results, and any challenges you faced.\n\nRemember, your final project should showcase your understanding of machine learning concepts and your ability to apply them to solve a real-world problem. Feel free to ask if you have any more questions! \n",
              ],
            },
          ]
        )

        # Prompt user for input and get response from chat session
        user_input = input("Please provide the input you would like me to process: ")
        response = chat_session.send_message(user_input)

        # Print the response from the model
        print(response.text)
