echo -e "${GREEN}|=======================|Setting up Virtual Environment|=======================|${NC}"
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt