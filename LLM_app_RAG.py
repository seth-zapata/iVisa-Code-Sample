# -*- coding: utf-8 -*-
# Author: Seth Zapata

# Import statements here are purposefully left vague for sensitivity concerns

import boto3 # Key SDK for using AWS Bedrock

import bedrock_client_factory
import enrich_query_factory
import data_retrieval_client_factory

# Add imports here for classes in other other files

class Search:
    def __init__(self, bedrock_client_factory, enrich_query_factory, data_retrieval_client_factory):

        # Can ignore, just an initialization of class variables denoting client instances.
        self.bedrock_client_factory = bedrock_client_factory
        self.enrich_query_factory = enrich_query_factory
        self.data_retrieval_client_factory = data_retrieval_client_factory

    def get_search_input(self, input):

        # Instantiate all necessary clients to perform operations
        bedrock_client = self.bedrock_client_factory.get_client()
        enrich_query = self.enrich_query_factory.get_enriched_query()
        data_retrieval_query = self.data_retrieval_client_factory.get_data_retrieval_query()

        # These would be stored in separate configuration files or retrieved secret keys
        token_count = "Hidden value"
        k_value = "Hidden value"
        p_value = "Hidden value"
        temp_value = "Hidden value"

        # Construct of LLM model hyper-parameters
        model_args = ModelArgs.builder() \
                              .max_token_count(token_count) \
                              .top_k(k_value) \
                              .top_p(p_value) \
                              .temperature(temp_value)

        # Create the LLM instance and model for database query generation from AWS Bedrock
        bedrock_instance = Bedrock(Model.Args.Model.CLAUDE_V2, bedrock_client, model_args)
        bedrock_db_query = DBQueryModel(ModelArgs.Model.CLAUDE_V2, bedrock_client, model_args)

        # Generated database query via specialized LLM (bedrock_db_query)
        retrieve_db_query = GenerateDBQueryAnswer.from_llm(bedrock_db_query)

        # Enrich query with additional context by querying user input with
        # a database. This could be a vector database with a similarity search
        # between the user input and relevant records found in the vector database.
        query_enrichment = enrich_query.get_enrichment_records(input.query)

        # Should also add logging on this vector database for potential errors, like null
        # records found, timeout exception, etc.

        # Using the enrichment records and user input, construct a query against a database
        # containing the needed information (could be SQLite, DynamoDB, ElasticSearch, etc.)
        generate_db_query = GenerateDBQueryAnswer(data_retrieval_query)
        generated_db_query_response = generate_db_query.generate(input.query, query_enrichment)

        # Should also add logging on this database for any potential errors, like incorrect query
        # generation, database request timeout, etc.

        # Here we get the actual records back from the database
        result_records = generate_db_query.return_list(query=generated_db_query, wait_time=wait_time, batch_size=batch_size)

        # Constructs the natural language LLM response mechanism
        get_final_response = GenerateFinalResponse.from_llm(bedrock_instance)

        # Uses the NL LLM response mechanism to generate a response based on the records
        # retrieved and the original user input. This allows LLM to form a reasonable response
        # which can be sent back to the user
        final_user_response = get_final_response.generate(input.query, generate_db_query, result_records)
        return {
            'db_query': generate_db_query,
            'response': final_user_response,
            'response_status': 'ANSWER_COMPLETE_SUCCESS' # Useful for logging efforts
        }

