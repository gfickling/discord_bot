'''Functions to help you'''
import json
import requests


def build_help_message(help_with, help_msg):
    '''Put together the right string to send back in reply to a "help" request'''
    if help_msg == 'help':
        prompt_string = list_to_string(help_with)
        prompts_help = 'I will answer questions with words that start contain ' + prompt_string + \
            'Other key words are "hello", "pup", and "inspire me". Type "commands" for a list of things you can update.'
        print(prompts_help)
        return prompts_help
    if help_msg == 'commands':
        command_string = list_to_string(help_with)
        print(command_string)
        return (command_string)
    else:
        return "Invalid help question)"


def check_dupe(m_client, value):
    '''Check for duplicate record in the database'''
    exists = m_client.answers.answers.count_documents(
        {'ans_lower': value.lower()})
    if exists != 0:
        return f"'{value}' already exists in the database"
    return False


def db_prompts(m_client, prompt):
    '''Call with argument "all" to return all prompts from the database.
        Any other argument checks if prompt exists and returns argument'''
    if prompt == "all":
        prompts_from_db = m_client.prompts.questions.find()
        return prompts_from_db
    prompt_exists = m_client.prompts.questions.find_one({"prompt": prompt})
    if prompt_exists is not None:
        return prompt_exists[prompt]
    else:
        return []


def get_answers(m_client):
    '''Gets all answers from database'''
    answers = m_client.answers.answers.find()
    replies, paras, one_liners = ([] for i in range(3))
    for i in answers:
        try:
            replies.append(i['reply'])
        except KeyError:
            pass
        try:
            paras.append(i['para'])
        except KeyError:
            pass
        try:
            one_liners.append(i['one_liner'])
        except KeyError:
            pass
    with open("answers.txt", "w") as f:
        f.write("\n\nReplies:\n\n")
        for r in replies:
            f.write(r)
            f.write("\n")
        f.write("\n\nParas:\n\n")
        for p in paras:
            f.write(p)
            f.write("\n")
        f.write("\n\nOne Liners:\n\n")
        for o in one_liners:
            f.write(o)
            f.write("\n")
    return replies, paras, one_liners


def get_quote():
    '''Gets a random quote from https://zenquotes.io/api/random'''
    response = requests.get('https://zenquotes.io/api/random')
    try:
        response.status_code == requests.codes.ok
        print(response.status_code)
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " - " + json_data[0]['a']
        print(quote)
        return (quote)
    except requests.exceptions.RequestException as e:
        print("Request Exception" + e)
        return ("Unable to inspire you right now, my source is down")


def list_to_string(list_name):
    '''This function converts a list to a punctuated string'''
    string = ""
    for index, p in enumerate(list_name):
        if index != len(list_name)-1:
            string += '"' + str(p) + '", '
        else:
            string += 'or "' + p + '". '
    return string


def update_answers(m_client, section, user_reply):
    '''Insert a user generated reply into the database'''
    to_add = {section: user_reply, 'ans_lower': user_reply.lower()}
    post_id = m_client.answers.answers.insert_one(to_add).inserted_id
    print(f'User reply {user_reply} added, id: {post_id}')
