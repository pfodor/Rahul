Use the generateSL.py and generateSP_new.py files to create data sets for alphabets of size strictly smaller than 10.
Use the generateSL_new.py and generateSP_new.py files to create data sets for alphabets of size bigger than or equal to 10.



Usage for generateSL.py

      python3 generateSL.py  alphabet sl_training_directory sl_testing_directory

      examples: python3 generateSL.py abcd sl_train4 sl_test4


Usage for generateSL_new.py generateSP_new.py

      python3 generateSL[SP]_new.py  Alphabet_Size sl[sp]_training_directory sl[sp]_testing_directory

      examples: python3 generateSL_new.py 50 sl_train50 sl_test50
      	        python3 generateSP_new.py 36 sp_train36 sp_test36



Once these seperate data files and directories have been created we combine them using the dataTransferScript and the dataCombineScript

First run dataTransferScript.py as follow:

      python3 dataTransferScript.py sl_training_directory sl_test_directory sp_train_directory sp_test_directory combineDirectory

      examples: python3 dataTransferScript.py sl_train4 sl_test4 sp_train4 sp_test4 Alphabet-4


Now move into the newly generated combined directory from the previous command.
    ex: cd Alphabet-4

Inside here we run ../dataCombineScript.sh


Now all the file inside Alphabet-4 should be combined appropriately to run with our exisiting chainer code.

