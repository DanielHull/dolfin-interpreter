REM this is a standard test
python dolfin_handler_cli.py "16115.results.csv" "C:\Users\dhull\Documents\code_directory\dolfininterpreter\test" --save_loc "C:\Users\dhull\Downloads"
REM this tests save name
python dolfin_handler_cli.py "16115.results.csv" "C:\Users\dhull\Documents\code_directory\dolfininterpreter\test" --output_name "save name test" --save_loc "C:\Users\dhull\Downloads
REM this tests normalization factor
python dolfin_handler_cli.py "16115.results.csv" "C:\Users\dhull\Documents\code_directory\dolfininterpreter\test" --output_name "normalization factor" --normalization_factor 2.0 --save_loc "C:\Users\dhull\Downloads"
REM this tests picking only a subset of drop numbers
python dolfin_handler_cli.py "16115.results.csv" "C:\Users\dhull\Documents\code_directory\dolfininterpreter\test" --output_name "drop numbers" --start_number 2 --end_number 5 --save_loc "C:\Users\dhull\Downloads"
REM this tests offset functionality
python dolfin_handler_cli.py "16115.results.csv" "C:\Users\dhull\Documents\code_directory\dolfininterpreter\test" --offset 1 3 --output_name "offset testing" --save_loc "C:\Users\dhull\Downloads"
REM this tests endpoint functionality 2
python dolfin_handler_cli.py "16116.results.csv" "C:\Users\dhull\Documents\code_directory\dolfininterpreter\test" --output_name "endpoint testing" --save_loc "C:\Users\dhull\Downloads"
REM this tests endpoint functionality 2
python dolfin_handler_cli.py "16116.results.csv" "C:\Users\dhull\Documents\code_directory\dolfininterpreter\test" --output_name "endpoint testing" --save_loc "C:\Users\dhull\Downloads"