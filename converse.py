from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import pinecone
from dotenv import load_dotenv
import os

load_dotenv()
pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="us-west4-gcp-free")
embeddings = OpenAIEmbeddings()
index_name = "testelon2"

retriever = Pinecone.from_existing_index(embedding=embeddings, index_name=index_name)
# retriever = doc_store.as_retriever()
# tool = create_retriever_tool(
#     retriever, "hotel_knowledge", "use this if any question about hotel"
# )
# tools = [tool]

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "act as a sales bot for hotel XYZ. Ask the user to provide name before querying. Say you don't know if you don't have the answer. Hotel xyz is located at 24 Windsor road W6 7TA. It has 200 rooms, one swimming pool and one restaurant called Super Spicy that can cater 100 guests.\n\n
            The below document is a template to generate a cover letter. A cover letter is generated when some asked about hiring a venue in hotel xyz or wanting to book a venue. Please replace the [] bracket with the name of the user.

Cover Letter:
[name]

Dear [name],
Thank you for considering hotel XYZ as the potential venue for your upcoming Holiday Party event. We're excited about the opportunity to collaborate and assist in making your event a memorable success.
We understand your requirements for hosting various activities, including a festive Award Ceremony for approximately 200 guests, Holiday-themed Board Meetings, a Conference Meet, a creative Trade Show event, a Team-Building Activity, and a Product Launching Event.
We're dedicated to providing you with the perfect spaces and resources to bring these elements to life.

In this proposal, you'll find that our venue's offerings align with your event's diverse needs. Our team is committed to ensuring your event's success and creating an atmosphere that reflects the spirit of the holiday season.
We look forward to the possibility of working together to make your Holiday Party event truly exceptional. Please feel free to contact us to discuss the details further.

Warm regards,
John Doe
Event Manager
Hotel XYZ

Proposal:
ABC Events' upcoming Holiday Party event offers an exciting opportunity to celebrate the festive season in style. With a focus on diverse activities, including an Award Ceremony, Board Meetings, Conference Meet, Trade Show, Team-Building Activity and Product Launching Event, the event promises to be engaging and memorable.
Hotel XYZ is well-equipped to cater to your event's specific needs, offering versatile spaces that can accommodate a range of activities. Our commitment to excellence ensures that each aspect of your event will be well-supported, allowing your attendees to fully immerse themselves in the holiday festivities.
Facilities:
A hall suitable for the festive Award Ceremony, accommodating around 200 guests.
Dedicated spaces for the Holiday-themed
Board Meetings and Conference Meet.
A creative Trade Show area designed to showcase products and services.
A versatile room for the Team-Building Activity to encourage collaboration and camaraderie.
A designated area for the Product Launching Event, complete with multimedia capabilities.

Event Planning:
Collaborative event planning and implementation services from pre-event preparations to the event's conclusion.
Detailed floor plans tailored to each activity's requirements.
Timelines, event expense reports, and coordination with in-house and external service providers.

Catering:
Customizable catering options, including holiday-themed menus.
Accommodation of dietary preferences and restrictions for a delightful dining experience.
Technology:
State-of-the-art audiovisual equipment to enhance presentations and interactions.
Accommodation:
Options for special rates on accommodations for event attendees requiring overnight stays.

Transportation:
Convenient transportation access for attendees.
With hotel XYZ's exceptional facilities, dedicated staff, and commitment to delivering high-quality events, your ABC Events' Holiday Party is poised to become a festive and memorable occasion. We're excited to collaborate with you to make this event a resounding success. Please don't hesitate to reach out for further discussions and planning.



            
            "
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{query}"),
    ]
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever.as_retriever(),
    verbose=True, memory = memory
)

while True:
    get_input = input("query : ")
    if get_input == "break":
        break
    result = chain.run(get_input)
    print(result)
