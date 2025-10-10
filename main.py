import os

def print_criterias(criterias):
    print("=============================Game Settings=================================")
    for criteria_nb, criteria in criterias.items():
        print(f'Criteria {criteria_nb}:\n{criteria["criteria"]}')
    print("===========================================================================\n")

def main():
    print("Welcome to the Turing Machine Board Game!")
    print("Input game set up (criteria cards and verification cards seperated by comas): ")
    game_setup = input().strip().split(",")
    print()

    # read datas
    with open(os.path.join('data', 'Criteria_Cards.txt'), 'r') as f:
        criteria_data = f.readlines()
        for i, line in enumerate(criteria_data):
            criteria_data[i] = line.strip()
    with open(os.path.join('data', 'Verification_Cards.txt'), 'r') as f:
        verification_date= f.readlines()
        for i, line in enumerate(verification_date):
            verification_date[i] = line.strip()
    with open(os.path.join('data', 'Punch_Cards.txt'), 'r') as f:
        punch_date = f.readlines()
        for i, line in enumerate(punch_date):
            punch_date[i] = line.strip()
    
    criterias = {}
    c_card_nb = 0
    v_card_nb = 0
    for card in game_setup:
        if card.isnumeric():
            # criteria card
            for i, line in enumerate(criteria_data):
                card_exists = False
                if line == f'C{card}':
                    criterias[c_card_nb] = {'criteria': f'\t{criteria_data[i+1]}\n\t{criteria_data[i+2]}\n\t{criteria_data[i+3]}\n'}
                    c_card_nb += 1
                    card_exists = True
                    break
            if not card_exists:
                print(f"Criteria card C{card} does not exist! Exiting...")
                return 0
        else:
            # verification card
            if v_card_nb >= c_card_nb:
                print("More verification cards than criteria cards! Exiting...")
                return 0
            for i, line in enumerate(verification_date):
                this_verification = ''
                card_exists = False
                if line == card:
                    j = i + 1
                    while not verification_date[j].isnumeric():
                        j += 1
                    for k in range(12):
                        this_verification += verification_date[j + k]
                    this_verification = int(this_verification, 2) # save as binary
                    criterias[v_card_nb]['verification'] = this_verification
                    v_card_nb += 1
                    card_exists = True
                    break
            if not card_exists:
                print(f"Verification card {card} does not exist! Exiting...")
                return 0
    
    print_criterias(criterias)
    
    # game loop
    nb_rounds = 1
    nb_checks = 1
    while True:
        if nb_rounds > 1:
            print('Do you need a reminder of the criterias? (y/N)')
            reminder = input().strip().lower()
            if reminder == 'y':
                print_criterias(criterias)
            elif reminder != 'n' and reminder != '':
                print("Invalid input, no reminder will be given.\n")
        print('-----------------------------New Round----------------------------------')
        print(f'Round: {nb_rounds}')
        print('Input a number to check:')
        number = input()

        # validate input
        if not number.isnumeric():
            print("Input must be a number\n")
            continue
        if len(number) != 3:
            print("Input number must be 3 digits long\n")
            continue
        valid = True
        for i in number:
            if int(i) < 1 or int(i) > 5:
                print("Each digit must be between 1 and 5\n")
                valid = False
                break
        if not valid:
            continue
        
        print()
        
        # find the punch card, store as binary number
        punch_card = int('1' * 144, 2)
        for i, digit in enumerate(number):
            this_card = 'xxx'
            this_card = this_card[:i] + digit + this_card[i+1:]
            for j, line in enumerate(punch_date):
                if line == this_card:
                    k = j + 1
                    this_punch = ''
                    for l in range(12):
                        this_punch += punch_date[k + l]
                    punch_card &= int(this_punch, 2)
                    break
        
        # check up to three criterias
        check_in_one_round = 0
        while check_in_one_round < 3:
            print('--------New Check--------')
            print(f'Total checks: {nb_checks}, checks in this round: {check_in_one_round + 1}')
            print('Input criteria number to check (if no checks anymore, press return without any input): ')
            criteria_nb_to_check = input().strip()
            
            # validate input
            if criteria_nb_to_check == '':
                break
            if not criteria_nb_to_check.isnumeric():
                print("Input must be a number\n")
                continue
            criteria_nb_to_check = int(criteria_nb_to_check)
            if criteria_nb_to_check < 0 or criteria_nb_to_check >= len(criterias):
                print("Input criteria number out of range\n")
                continue
            
            # check result
            result = punch_card & criterias[criteria_nb_to_check]['verification']
            if result:
                print(f'Criteria {criteria_nb_to_check} is satisfied!\n')
            else:
                print(f'Criteria {criteria_nb_to_check} is NOT satisfied!\n')

            check_in_one_round += 1
            nb_checks += 1

        nb_rounds += 1

if __name__ == "__main__":
    main()