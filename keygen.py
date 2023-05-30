words = [
    "Industry", "Ultimate", "Favorite", "Strategy", "Stronger", "Training", "Terminal", "Positive", "Together",
    "Language", "Research", "Economy", "Solution", "Platform", "Building", "Software", "Security", "Hospital",
    "Standard", "Creative", "Mountain", "Instance", "Generate", "Activate", "Friendly", "Increase", "Business",
    "Hospital", "Personal", "Discover", "Internet", "Advanced", "Complete", "Critical", "Exchange", "Analysis",
    "Activate", "Friendly", "Increase", "Business", "Hospital", "Personal", "Discover", "Internet", "Advanced",
    "Complete", "Critical", "Exchange", "Analysis", "Reaction", "Together", "Security", "Hospital", "Standard",
    "Creative", "Mountain", "Instance", "Generate", "Activate", "Friendly", "Increase", "Business", "Hospital",
    "Personal", "Discover", "Internet", "Advanced", "Complete", "Critical", "Exchange", "Analysis", "Reaction",
    "Solution", "Strategy", "Training", "Terminal", "Positive", "Together", "Language", "Research", "Economy",
    "Favorite", "Industry", "Ultimate", "Favorite", "Strategy", "Stronger", "Training", "Terminal", "Positive",
    "Together", "Language", "Research", "Economy", "Solution", "Platform", "Building", "Software", "Security",
    "Hospital", "Standard", "Creative", "Mountain", "Instance", "Generate", "Activate", "Friendly", "Increase",
    "Business", "Hospital", "Personal", "Discover", "Internet", "Advanced", "Complete", "Critical", "Exchange",
    "Analysis", "Reaction", "Together", "Security", "Hospital", "Standard", "Creative", "Mountain", "Instance",
    "Generate", "Activate", "Friendly", "Increase", "Business", "Hospital", "Personal", "Discover", "Internet",
    "Advanced", "Complete", "Critical", "Exchange", "Analysis", "Reaction", "Solution", "Strategy", "Training",
    "Terminal", "Positive", "Together", "Language", "Research", "Economy", "Favorite", "Industry", "Ultimate",
    "Favorite"
]

def generate_integers(string):
    import hashlib
    hash_value = hashlib.sha256(string.encode()).hexdigest()

    hash_int = int(hash_value, 16)

    integers = []
    for _ in range(4):
        integer = hash_int % 128
        integers.append(integer)
        hash_int = hash_int // 128

    return integers

def getKeyFromStr(phrase):
    wordIndex = generate_integers(phrase)
    key = ""
    for word in wordIndex:
        key += words[word]
    return(key)