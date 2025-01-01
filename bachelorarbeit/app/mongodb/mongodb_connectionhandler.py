from pymongo import MongoClient

class MongoDBConnectionHandler:
    """
    A class for managing connections to a MongoDB database.
    """
    def __init__(self, database_name):
        """
        Initializes a MongoDBConnectionHandler object.

        Parameters:
        - database_name (str): The name of the MongoDB database.
        """
        self.client = MongoClient("HIDDEN")
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        """
        Retrieves a MongoDB collection.

        Parameters:
        - collection_name (str): The name of the collection.

        Returns:
        - pymongo.collection.Collection: The MongoDB collection.
        """
        return self.db[collection_name]

    def create_collection(self, collection_name):
        """
        Creates a new MongoDB collection.

        Parameters:
        - collection_name (str): The name of the new collection.

        Returns:
        - str: A message indicating the success of the collection creation.
        """
        self.db.create_collection(collection_name)
        return f"Collection '{collection_name}' created successfully."
    
    def find_document_by_category(self, collection_name, category):
        """
        Finds a document in a collection based on the specified category.

        Parameters:
        - collection_name (str): The name of the collection.
        - category (str): The category to search for in the documents.

        Returns:
        - dict or None: The document if found, otherwise None.
        """
        collection = self.get_collection(collection_name)
        document = collection.find_one({"category": category})
        return document
    
    def find_all_documents_by_category(self, collection_name, category):
        """
        Finds all documents in a collection based on the specified category.

        Parameters:
        - collection_name (str): The name of the collection.
        - category (str): The category to search for in the documents.

        Returns:
        - pymongo.cursor.Cursor: A cursor containing all documents matching the category.
        """
        collection = self.get_collection(collection_name)
        documents = collection.find({"category": category})
        return documents

    def insert_or_update_document(self, collection_name, category, data):

        """
        Inserts a document or updates an existing document with the specified category.

        Parameters:
        - category (str): The category of the document.
        - data (dict): The document data to be inserted or updated.

        Returns:
        - str: A message indicating the success of the operation.
        """
        collection = self.get_collection(collection_name)

        # Check if a document with the specified category already exists
        existing_document = self.find_document_by_category(collection_name, category)

        if existing_document:
            # If a document exists, update it
            collection.update_one({"category": category}, {"$set": data})
            return f"Document with category '{category}' updated successfully."
        else:
            # If no document exists, insert a new one
            collection.insert_one(data)
            return f"Document with category '{category}' inserted successfully."
    
    def populate_database(self):
        COLLECTION_NAME = "categories"
        management = {
            "category": "management",
            "sentiments": {
                "positive": [
                    "The student took the lead on the project, delivered everything on time, continuously identified important action points, organized meetings with the supervisors and came prepared to them..",
                    "The student took the initiative to create a detailed project plan, outlining milestones and deadlines, and consistently adhered to the established timeline.",
                    "Recognizing the significance of effective communication, the student kept all project documentation well-organized and accessible, fostering clear and transparent communication with supervisors."
                ],
                "neutral": [
                    "The student independently managed the project, adhering to the established timeline and completing tasks as required.",
                    "In project management, the student took on the responsibility of coordinating tasks and ensuring that deadlines were met."
                ],
                "negative": [
                    "The student struggled to meet deadlines and failed to deliver key project components on time.",
                    "The student exhibited a lack of initiative in proactively addressing project challenges, resulting in delays and setbacks.",
                    "The solo project undertaken by the student faced issues due to poor organization and a failure to anticipate potential obstacles."
                ]
            }
        }

        difficulty = {
            "category": "difficulty",
            "sentiments": {
                "positive": [
                    "The project was very challenging. The student had to think outside of the box and do some research to fulfil the project's requirements.",
                    "Navigating through the complex aspects of the project provided an excellent opportunity for growth and skill development."
                ],
                "neutral": [
                    "The project presented a moderate level of difficulty, requiring standard problem-solving skills and a systematic approach."
                ],
                "negative": [
                    "The project was not complicated enough. It lacked the depth and complexity needed to fully engage skills and expertise."
                ]
            }
        }

        originality = {
            "category": "originality",
            "sentiments": {
                "positive": [
                    "The project was extraordinarily original. The student developed an innovative solution.",
                    "The creative approach taken by the student set the project apart from others."
                ],
                "neutral": [
                    "The project's originality aligns with the expectations, incorporating some unique elements.",
                    "The team introduced original contributions to the project, meeting the expected level of innovation."
                ],
                "negative": [
                    "While the project includes some unique aspects, the overall originality falls short of expectations.",
                    "The project's originality is compromised by a lack of innovative ideas and fails to stand out in a meaningful way."
                ]
            }
        }

        applicability = {
            "category": "applicability",
            "sentiments": {
                "positive": [
                    "The presented project is highly applicable. The project aims to solve current issues which are presented and discussed in the introduction of the Thesis.",
                    "The practical implications of this project are significant, addressing real-world problems and providing valuable solutions.",
                    "The proposed solutions are well-aligned with the identified challenges, making the project highly applicable in the given context."
                ],
                "neutral": [
                    "While the project addresses certain issues, its overall applicability remains to be fully explored.",
                    "The level of applicability is not clearly defined in the available details of the project."
                ],
                "negative": [
                    "The project's applicability is questionable, as it doesn't seem to effectively address the core issues outlined in the introduction.",
                    "Despite the effort, the project lacks practical relevance to the discussed problems, raising concerns about its applicability.",
                    "The proposed solutions may not be applicable in a broader context, limiting the overall impact of the project."
                ]
            }
        }


        readability = {
            "category": "readability",
            "sentiments": {
                "positive": [
                    "The structure is consistently comprehensible and purposeful, in line with the interest the task, and contributes to comprehension. The linguistic expression is consistently fact-oriented with an appropriate choice of words and precise formulations. Technical terms are used consistently, precisely and in relation to the scientific discourse. The text is free of errors.",
                    "The document's readability is excellent, with a well-organized structure and clear language that enhances understanding. The use of technical terms is appropriate and enhances the overall clarity of the text.",
                    "The text is easy to follow, with a well-thought-out structure and language that aids in effective communication. The absence of errors contributes to the overall readability of the content."
                ],
                "neutral": [
                    "The document's readability is not explicitly discussed in the provided information.",
                    "While a structure is present, the overall readability is not very clear."
                ],
                "negative": [
                    "The document's readability is a concern, as the structure and language used may hinder comprehension. The text lacks clarity and precision in its expression.",
                    "There are issues with readability, as the document's structure is unclear and the language used is not conducive to effective communication. Technical terms are either misused or not appropriately integrated into the text.",
                    "The presence of errors in the text significantly affects its readability. The document requires careful proofreading and editing to improve overall clarity."
                ]
            }
        }

        requirements = {
            "category": "requirements",
            "sentiments": {
                "positive": [
                    "The student researched and identified the requirements for the project to be successful. Either the student extracted them from the state-of-the-art or from possible users of the proposed solution. Requirements are clearly described.",
                    "The project's requirements are well-researched and clearly articulated, demonstrating a thorough understanding of the key factors necessary for success.",
                    "A commendable effort has been made to identify and describe the project's requirements, showcasing a strong foundation for the proposed solution."
                ],
                "neutral": [
                    "The discussion on requirements is not explicitly presented in the provided information.",
                    "There might be requirements for the project, but they are not clearly defined or discussed in the available details."
                ],
                "negative": [
                    "There are concerns about the adequacy of the project's requirements. The identification and description of requirements may lack depth and specificity.",
                    "The project's requirements are inadequately addressed, and the information provided is insufficient for a comprehensive understanding of the necessary elements for success.",
                    "The lack of clarity in the presentation of requirements raises questions about the project's foundational understanding and planning."
                ]
            }
        }

        design = {
            "category": "design",
            "sentiments": {
                "positive": [
                    "The developed system architecture includes state-of-the-art components and meets the requirements of the proposed solution. Considerations of design alternatives were present. The system design is clearly described.",
                    "The system architecture demonstrates a commitment to utilizing cutting-edge components, aligning well with the requirements of the proposed solution. The inclusion of design alternatives adds depth to the overall design process.",
                    "A commendable effort has been made to provide a clear and detailed description of the system design, showcasing a thoughtful consideration of design alternatives and adherence to project requirements."
                ],
                "neutral": [
                    "While there may be a system design, it is not clearly defined.",
                    "The details regarding the system design require further exploration for a comprehensive understanding."
                ],
                "negative": [
                    "There are concerns about the adequacy of the system design. The description lacks clarity, and there are insufficient considerations of design alternatives.",
                    "The system design is inadequately addressed, and the information provided is insufficient for a comprehensive understanding of the design choices made.",
                    "The lack of clarity in the presentation of the system design raises questions about the project's foundational design principles and decision-making process."
                ]
            }
        }

        implementation = {
            "category": "implementation",
            "sentiments": {
                "positive": [
                    "The implementation works smoothly; it is fully functional. The code for the implementation is available, well-explained, and documented.",
                    "The implementation demonstrates a high level of functionality, and the availability of well-explained and documented code adds value to the overall project.",
                    "An impressive effort has been made to ensure a smooth and fully functional implementation. The clarity of the code and documentation enhances the project's overall quality."
                ],
                "neutral": [
                    "There are concerns about the implementation, but it is fully functional.",
                    "While there may be an implementation, it is not clearly discussed in the work.",
                    "The details regarding the implementation require further explanations for a comprehensive understanding."
                ],
                "negative": [
                    "There are concerns about the implementation's functionality. The description may lack clarity, and there could be issues with the code's performance.",
                    "The implementation is inadequately addressed, and the information provided is insufficient for a comprehensive understanding of its functionality.",
                    "The lack of clarity in the presentation of the implementation raises questions about the project's overall execution and success in meeting its objectives."
                ]
            }
        }
        self.insert_or_update_document(COLLECTION_NAME, management["category"], management)
        self.insert_or_update_document(COLLECTION_NAME, difficulty["category"], difficulty)
        self.insert_or_update_document(COLLECTION_NAME, originality["category"], originality)
        self.insert_or_update_document(COLLECTION_NAME, applicability["category"], applicability)
        self.insert_or_update_document(COLLECTION_NAME, readability["category"], readability)
        self.insert_or_update_document(COLLECTION_NAME, requirements["category"], requirements)
        self.insert_or_update_document(COLLECTION_NAME, design["category"], design)
        self.insert_or_update_document(COLLECTION_NAME, implementation["category"], implementation)

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()



if __name__ == "__main__":
    # TESTING PURPOSES
    DATABASE_NAME = "database"
    COLLECTION_NAME = "categories"
    connection_handler = MongoDBConnectionHandler(DATABASE_NAME)
    connection_handler.populate_database()
