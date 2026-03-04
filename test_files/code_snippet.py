# Sample Python Code for Testing


class WeatherAnalyzer:
    """A class to analyze weather data"""

    def __init__(self, city):
        self.city = city
        self.temperatures = []

    def add_temperature(self, temp):
        """Add a temperature reading"""
        self.temperatures.append(temp)

    def get_average(self):
        """Calculate average temperature"""
        if not self.temperatures:
            return 0
        return sum(self.temperatures) / len(self.temperatures)

    def get_max(self):
        """Get maximum temperature"""
        return max(self.temperatures) if self.temperatures else None

    def get_min(self):
        """Get minimum temperature"""
        return min(self.temperatures) if self.temperatures else None

    def analyze(self):
        """Provide weather analysis"""
        avg = self.get_average()
        max_temp = self.get_max()
        min_temp = self.get_min()

        return {
            "city": self.city,
            "average": avg,
            "max": max_temp,
            "min": min_temp,
            "range": max_temp - min_temp if max_temp and min_temp else 0,
        }


# Usage example
analyzer = WeatherAnalyzer("Delhi")
analyzer.add_temperature(25)
analyzer.add_temperature(30)
analyzer.add_temperature(28)
analyzer.add_temperature(32)

result = analyzer.analyze()
print(f"Weather Analysis for {result['city']}:")
print(f"Average: {result['average']:.1f}°C")
print(f"Max: {result['max']}°C")
print(f"Min: {result['min']}°C")
print(f"Range: {result['range']}°C")
