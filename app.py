from rag import invoke_graph

response = invoke_graph("Wrong feature flag set for Reporting; users in us-west-2 see incomplete menu.")
print(response)