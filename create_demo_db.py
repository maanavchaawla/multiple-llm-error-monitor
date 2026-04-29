{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "dacfcd87-c267-4e51-a365-bbb9203bf866",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Successfully created 'error_logs.xlsx' with demo data!\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "# Define the sample data (I've added two extra errors so you can test multiple emails!)\n",
    "data = {\n",
    "    \"Error_ID\": [\"ERR-001\", \"ERR-002\", \"ERR-003\"],\n",
    "    \"Timestamp\": [\"2024-10-24 10:00:00\", \"2024-10-24 10:15:30\", \"2024-10-24 10:45:12\"],\n",
    "    \"Error_Type\": [\"DatabaseConnectionError\", \"AuthenticationFailure\", \"TimeoutError\"],\n",
    "    \"Description\": [\n",
    "        \"Timeout expired. The timeout period elapsed prior to completion of the operation or the server is not responding. Port 5432.\",\n",
    "        \"Invalid API key provided for the external payment gateway service.\",\n",
    "        \"Internal microservice request to the inventory database took longer than 5000ms.\"\n",
    "    ],\n",
    "    \"Status\": [\"Pending\", \"Pending\", \"Pending\"]\n",
    "}\n",
    "\n",
    "# Create a Pandas DataFrame\n",
    "df = pd.DataFrame(data)\n",
    "\n",
    "# Save it as an Excel file\n",
    "file_name = \"error_logs.xlsx\"\n",
    "df.to_excel(file_name, index=False)\n",
    "\n",
    "print(f\"✅ Successfully created '{file_name}' with demo data!\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
