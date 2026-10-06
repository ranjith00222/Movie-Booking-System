# Movie information is stored in dictionaries, using each movie's number as its key.
movies = {
    1: {"name": "Kalki 2898 AD", "time": "10:00 AM", "price": 150},
    2: {"name": "RRR", "time": "2:00 PM", "price": 200},
    3: {"name": "Interstellar", "time": "6:30 PM", "price": 250},
}

# Theatre numbers connect each cinema with its Hyderabad location.
theatres = {
    1: {"name": "AMB Cinemas", "location": "Gachibowli"},
    2: {"name": "Prasads Multiplex", "location": "Khairatabad"},
    3: {"name": "PVR RK Cineplex", "location": "Banjara Hills"},
    4: {"name": "INOX GVK One", "location": "Banjara Hills"},
    5: {"name": "PVR Nexus Mall", "location": "Kukatpally"},
    6: {"name": "AAA Cinemas", "location": "Ameerpet"},
    7: {"name": "Allu Cinemas", "location": "Kokapet"},
    8: {"name": "ART Cinemas", "location": "Vanasthalipuram"},
    9: {"name": "MovieMax AMR", "location": "ECIL"},
    10: {"name": "GPR Multiplex", "location": "Nizampet"},
}

# These settings control seat rows, columns, and how many tickets one person can book.
ROWS = 5
COLS = 6
MIN_TICKETS = 1
MAX_TICKETS = 5

# Store a separate seat map for each theatre and movie. O means available; X means booked.
seats = {}
for theatre_id in theatres:
    seats[theatre_id] = {}
    for movie_id in movies:
        seats[theatre_id][movie_id] = []
        for row in range(ROWS):
            seats[theatre_id][movie_id].append(["O"] * COLS)

# Add sample pre-bookings to each movie at every theatre.
for theatre_id in theatres:
    seats[theatre_id][1][0][0] = "X"  # Kalki 2898 AD: seat A1
    seats[theatre_id][2][2][3] = "X"  # RRR: seat C4
    seats[theatre_id][3][4][5] = "X"  # Interstellar: seat E6

# New bookings are kept in memory while the program is running.
bookings = {}
next_booking_id = 1001


# Display movies with their show times and ticket prices.
def show_movies():
    print("\nAVAILABLE MOVIES")
    for movie_id, movie in movies.items():
        print(f"{movie_id}. {movie['name']} | {movie['time']} | Rs.{movie['price']}")


# Display all theatres and their locations.
def show_locations():
    print("\nHYDERABAD THEATRE LOCATIONS")
    for theatre_id, theatre in theatres.items():
        print(f"{theatre_id}. {theatre['name']} - {theatre['location']}")


# Show a theatre's seat grid for the selected movie.
def show_seats(theatre_id, movie_id):
    print("\n       1   2   3   4   5   6")
    for row in range(ROWS):
        row_letter = chr(65 + row)
        print(f"  {row_letter}  | " + "   ".join(seats[theatre_id][movie_id][row]))
    print("O = Available, X = Booked")


# Keep asking until the user types a number from the provided options.
def get_choice(prompt, valid_choices):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_choices:
                return choice
            print("That number is not in the list. Try again.")
        except ValueError:
            print("Please enter a number.")


# Convert a row letter or number to its list position (A/1 becomes 0).
def get_row():
    while True:
        row_input = input("Enter row (A-E or 1-5): ").strip().upper()
        if row_input in ["A", "B", "C", "D", "E"]:
            return ord(row_input) - 65
        if row_input.isdigit() and 1 <= int(row_input) <= ROWS:
            return int(row_input) - 1
        print("Enter a row from A to E, or from 1 to 5.")


# Return the zero-based seat column after checking its number.
def get_seat_number():
    while True:
        try:
            seat_number = int(input("Enter seat number (1-6): "))
            if 1 <= seat_number <= COLS:
                return seat_number - 1
            print("Seat number must be between 1 and 6.")
        except ValueError:
            print("Please enter a number.")


# Choose a theatre, movie, ticket count, and available seats; then save one booking.
def book_ticket():
    global next_booking_id

    show_locations()
    theatre_id = get_choice("Enter theatre number: ", theatres)
    theatre = theatres[theatre_id]

    show_movies()
    movie_id = get_choice("Enter movie number: ", movies)
    movie = movies[movie_id]

    ticket_count = get_choice(
        f"Enter number of tickets ({MIN_TICKETS}-{MAX_TICKETS}): ",
        range(MIN_TICKETS, MAX_TICKETS + 1),
    )
    show_seats(theatre_id, movie_id)

    # Collect distinct available seats. Invalid or repeated choices are asked again.
    selected_seats = []
    while len(selected_seats) < ticket_count:
        print(f"\nSelect seat for ticket {len(selected_seats) + 1}.")
        row = get_row()
        column = get_seat_number()
        seat_name = chr(65 + row) + str(column + 1)

        if seats[theatre_id][movie_id][row][column] == "X":
            print(f"Seat {seat_name} is already booked. Choose another seat.")
        elif seat_name in selected_seats:
            print(f"Seat {seat_name} is already selected. Choose another seat.")
        else:
            selected_seats.append(seat_name)
            print(f"Seat {seat_name} selected.")

    # Mark selected seats as booked and calculate the full ticket cost.
    for seat_name in selected_seats:
        row = ord(seat_name[0]) - 65
        column = int(seat_name[1:]) - 1
        seats[theatre_id][movie_id][row][column] = "X"

    total_price = ticket_count * movie["price"]
    bookings[next_booking_id] = {
        "movie_id": movie_id,
        "movie": movie["name"],
        "show_time": movie["time"],
        "theatre_id": theatre_id,
        "theatre": theatre["name"],
        "location": theatre["location"],
        "tickets": ticket_count,
        "seats": selected_seats,
        "price": movie["price"],
        "total": total_price,
    }

    # Show the receipt and then advance the ID for the next booking.
    print("\nBOOKING CONFIRMED")
    print(f"Booking ID: {next_booking_id}")
    print(f"Movie: {movie['name']} | Time: {movie['time']}")
    print(f"Theatre: {theatre['name']} | Location: {theatre['location']}")
    print(f"Tickets: {ticket_count} | Seats: {', '.join(selected_seats)}")
    print(f"Price per ticket: Rs.{movie['price']} | Total: Rs.{total_price}")
    next_booking_id += 1


# List all bookings made since the program started.
def view_bookings():
    if not bookings:
        print("\nNo bookings available.")
        return

    print("\nALL BOOKINGS")
    for booking_id, booking in bookings.items():
        print(
            f"ID {booking_id}: {booking['movie']} at {booking['show_time']} | "
            f"{booking['theatre']} ({booking['location']})"
        )
        print(
            f"Tickets: {booking['tickets']} | Seats: {', '.join(booking['seats'])} | "
            f"Total: Rs.{booking['total']}"
        )


# Delete a booking and return its seats to the available state.
def cancel_ticket():
    if not bookings:
        print("\nNo bookings available to cancel.")
        return

    view_bookings()
    booking_id = get_choice("Enter booking ID to cancel: ", bookings)
    booking = bookings[booking_id]

    for seat_name in booking["seats"]:
        row = ord(seat_name[0]) - 65
        column = int(seat_name[1:]) - 1
        seats[booking["theatre_id"]][booking["movie_id"]][row][column] = "O"

    del bookings[booking_id]
    print(f"Booking {booking_id} cancelled. Refund: Rs.{booking['total']}")


# Repeat the menu until the user chooses Exit.
def main():
    while True:
        print("\nMOVIE TICKET BOOKING SYSTEM")
        print("1. Show Movies")
        print("2. Show Theatre Locations")
        print("3. Book Ticket")
        print("4. View Bookings")
        print("5. Cancel Ticket")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            show_movies()
        elif choice == "2":
            show_locations()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            view_bookings()
        elif choice == "5":
            cancel_ticket()
        elif choice == "6":
            print("Thank you for using the Movie Ticket Booking System!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


# Start the menu only when this file is run directly.
if __name__ == "__main__":
    main()