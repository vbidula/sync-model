DIR = libc/

all: Psync

Psync: libc/Psync.so

libc/%.so: libc/%.o
	$(CC) -o $@ -shared $<

libc/%.o: libc/%.c
	$(CC) -fPIC -o $@ -c $<


clean:
	@rm -f libc/*.so libc/*.o
