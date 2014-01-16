# Where is the source file for the .o file we want to build?
SOURCENAME="`find ../src -name "$2".c | head -1`"

if [ -z "$SOURCENAME" ]; then
	error "Can't find source for $1"
fi

gcc -o "$3" -c "$SOURCENAME"
