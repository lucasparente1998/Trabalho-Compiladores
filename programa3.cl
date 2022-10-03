(* This file presents a fairly large example of Cool programming. The
class List defines the names of standard list operations ala Scheme:
car, cdr, cons, isNil, rev, sort, rcons (add an element to the end of
the list), and print_list. In the List class most of these functions
are just stubs that abort if ever called. The classes Nil and Cons
inherit from List and define the same operations, but now as
appropriate to the empty list (for the Nil class) and for cons cells (for
the Cons class).

The Main class puts all of this code through the following silly 
test exercise:

 1. prompt for a number N
 2. generate a list of numbers 0..N-1
 3. reverse the list
 4. sort the list
 5. print the sorted list

Because the sort used is a quadratic space insertion sort, sorting
moderately large lists can be quite slow. *)

class List inherits IO { 
 (* Since abort() returns Object, we need something of
	 type Bool at the end of the block to satisfy the typechecker. 
 This code is unreachable, since abort() halts the program. *)
	isNil() : Bool { { abort(); true; } };

	cons(hd : Int) : Cons {
	 (let new_cell : Cons <- new Cons in
		new_cell.init(hd,self)
	 )
	};

	(* 
	 Since abort "returns" type Object, we have to add
	 an expression of type Int here to satisfy the typechecker.
	 This code is, of course, unreachable.
 *)
	car() : Int { { abort(); new Int; } };

	cdr() : List { { abort(); new List; } };

	rev() : List { cdr() };

	sort() : List { cdr() };

	insert(i : Int) : List { cdr() };

	rcons(i : Int) : List { cdr() };
	
	print_list() : Object { abort() };
};

class Cons inherits List {
	xcar : Int; -- We keep the car in cdr in attributes. --
	xcdr : List; 

	isNil() : Bool { false };

	init(hd : Int, tl : List) : Cons {
	 {
	 xcar <- hd;
	 xcdr <- tl;
	 self;
	 }
	};
	 
	car() : Int { xcar };

	cdr() : List { xcdr };
    };