from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from backend import run_travel_agent



# res = tavily_search("Best hotels in India")


# res = search_flights("Plan a 7 days Banglore trip from Pune")


user_input = input("Enter travel request: ")

res = run_travel_agent(
    user_input=user_input,
    thread_id="test_user"
)

print("\nFINAL RESPONSE:\n")
print(res["answer"])