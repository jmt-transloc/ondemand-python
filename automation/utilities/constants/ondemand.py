from typing import List


class Admin:
    """Constants for the OnDemand Admin application."""

    NAVIGATION_TABS: List[str] = ['Rides', 'Reports', 'Resources', 'Services', 'Dispatch']
    REPORTS_CHARTS: List[str] = [
        'Rides by Status',
        'Rides by Hour',
        'Ride Duration',
        'Ride Wait Time',
        'Total Passengers',
        'Vehicle Mileage',
        'Total Mileage',
        'Origins & Destinations',
        'Fare Payment',
        'Operator Metrics',
        'Performance Metrics',
    ]
    RESOURCES_TABS: List[str] = ['Settings', 'Addresses', 'Devices', 'Regions', 'Users', 'Vehicles']
    RIDE_FILTERS: List[str] = ['Upcoming', 'Complete', 'In Progress', 'Needs Attention']
    RIDES_TABS: List[str] = [
        'All Single Rides',
        'Pending Approval',
        'Requested',
        'On Vehicle',
        'Complete',
        'Canceled',
        'No Show',
        'Denied',
        'Active',
        'Upcoming',
    ]
    UPLOAD_NON_USER_MESSAGE: str = '10 users could not be added'
    UPLOAD_USER_FAILURE: str = 'Unable to process user upload list.'


class Web:
    """Constants for the OnDemand Web application."""

    NAVIGATION_TABS: List[str] = [
        'Book a Ride',
        'Agency',
        'My Addresses',
        'My Rides',
        'Profile',
        'Help',
        'Logout',
    ]
