HOVER_CLAIM = ''''Decompose complex claims based on first-order predicate logic without changing the meaning of the claim. Return decomposition results and the combination logic. Allowed logic labels are "AND","OR","NAND","NOR". Several examples are given here and you generate the result for the last complex claim.

# The complex claim is that Before I Go to Sleep stars an Australian actress, producer and occasional singer.
def simple claims():
    stars(Before I Go to Sleep,an Australian actress):"Before I Go to Sleep stars an Australian actress."
    producer and occasional singer(Australian actress):"The Australian actress is a producer and occasional singer."
    COMBINATION LOGIC:AND

# The complex claim is that Howard University Hospital and Providence Hospital are both located in Washington, D.C.
def simple claims():
    located(Howard University,Washington, D.C):"Howard University Hospital is located in Washington, D.C."
    located(Providence Hospital,Washington, D.C):"Providence Hospital is located in Washington, D.C."
    COMBINATION LOGIC:AND
    
# The complex claim is that WWE Super Tuesday took place at an arena that currently goes by the name TD Garden.
def simple claims():
    took place(WWE Super Tuesday,an arena):"The WWE Super Tuesday took place at an arena."
    goes by(an arena,the name TD Garden):"That arena currently goes by the name TD Garden."
    COMBINATION LOGIC:AND

# The complex claim is that Carnegie Hall Tower is located in the same city as Staten Island.
def simple claims():
    located(Carnegie Hall Tower,Staten Island):"Carnegie Hall Tower is located in the same city as Staten Island."
    COMBINATION LOGIC:AND

# The complex claim is that Talking Heads, an American rock band that was one of the most critically accomplex claimed bands of the 80s is featured in KSPNs AAA format.
def simple claims():
    American rock band(Talking Heads):"Talking Heads is an American rock band."
    one of the most critically accomplex claimed bands of the 80s(Talking Heads):"Talking Heads was one of the most critically accomplex claimed bands of the 80s."
    featured(Talking Heads,KSPNs AAA format):"Talking Heads is featured in KSPNs AAA format."
    COMBINATION LOGIC:AND
    
# The complex claim is that An IndyCar race driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season.
def simple claims():
    drove(An IndyCar race driver,a kind of Formula 1 car):"An IndyCar race driver drove a Formula 1 car."
    designed(Peter McCool,a Formula 1 car):"Peter McCool designed this Formula 1 car during the 2007 Formula One season."
    COMBINATION LOGIC:AND
       
# The complex claim is that Gina Bramhill was born in a village. The 2011 population of the area that includes this village was 167,446.
def simple claims():
    born(Gina Bramhill,a village):"Gina Bramhill was born in a village."
    167446(The 2011 population of the area that includes this village):"The 2011 population of the area that includes this village was 167,446."
    COMBINATION LOGIC:AND
    
# The complex claim is that The star of the Irish film directed by Paddy Breathnach played Marcus Agrippa in the HBO drama series \"Rome\".
def simple claims():
    directed by(Irish film,Paddy Breathnach):"The Irish film was directed by Paddy Breathnach."
    played(The star of the Irish film,Marcus Agrippa):"The star of the Irish film played Marcus Agrippa in the HBO drama series \"Rome\"."
    COMBINATION LOGIC:AND

# The complex claim is that Stephen King wrote the novel that the movie directed by Stanley Kubrick that was sampled in the album \"Where Blood and Fire Bring Rest\" was based on.
def simple claims():
    write(Stephen King,the novel):"Stephen King wrote the novel."
    based(the movie directed by Stanley Kubrick,the novel):"The movie directed by Stanley Kubrick was based on the novel."
    sampled(the movie directed by Stanley Kubrick,album \"Where Blood and Fire Bring Rest\"):"The movie directed by Stanley Kubrick was sampled in the album \"Where Blood and Fire Bring Rest\"."
    COMBINATION LOGIC:AND
    
# The complex claim is that Gael and Fitness are not published in the same country.
def simple claims():
    published(Gael,Fitness):"Gael and Fitness are not published in the same country."
    COMBINATION LOGIC:AND
        
# The complex claim is that In the 2004 Hockey film produced by a former major league baseball pitcher Kurt Russell played the USA coach.
def simple claims():
    produced(a former major league baseball pitcher,2004 Hockey film):"A former major league baseball pitcher produced the 2004 Hockey film."
    played(Kurt Russell,USA coach):"Kurt Russell played the USA coach in this film."
    COMBINATION LOGIC:AND
    
# The complex claim is that Along with the New York Islanders and the New York Rangers, the New Jersey Devils NFL franchise is popular in the New York metropolitan area.
def simple claims():
    popular(New York Islanders and the New York Rangers):"The New York Islanders and the New York Rangers are popular in the New York metropolitan area."
    popular(New Jersey Devils NFL franchise):"The New Jersey Devils NFL franchise is popular in the New York metropolitan area."
    COMBINATION LOGIC:AND
    
# The complex claim is that Eatza Pizza and Your Pie were not founded in the same state.
def simple claims():
    founded(Eatza Pizza and Your Pie):"Eatza Pizza and Your Pie were not founded in the same state."
    COMBINATION LOGIC:AND
    
# The complex claim is that The song recorded by Fergie that was produced by Polow da Don and was followed by Life Goes On was M.I.L.F.$.
def simple claims():
    recorded by(The song M.I.L.F.$,Fergie):"M.I.L.F.$ was recorded by Fergie."
    produced by(Fergie,Polow da Don):"Fergie was produced by Polow da Don."
    followed by(The song M.I.L.F.$,Life Goes On):"M.I.L.F.$ was was followed by Life Goes On."
    COMBINATION LOGIC:AND
    
# The complex claim is that Gregg Rolie and Rob Tyner, are not a keyboardist.
def simple claims():
    not a keyboardist(Gregg Rolie):"Gregg Rolie is not a keyboardist."
    not a keyboardist(Rob Tyner):"Rob Tyner is not a keyboardist."
    COMBINATION LOGIC:AND
    
# The complex claim is that Maria Esther Andion Bueno, not Jimmy Connors, is the player that is from Brazil.
def simple claims():
    the player from Brazil(Maria Esther Andion Bueno):"Maria Esther Andion Bueno is the player from Brazil."
    not the player from Brazil(Jimmy Connors):"Jimmy Connors is not the player from Brazil."
    COMBINATION LOGIC:AND
    
# The complex claim is that Vladimir Igorevich Arnold died after Georg Cantor.
def simple claims():
    died(Vladimir Igorevich Arnold,Georg Cantor):"Vladimir Igorevich Arnold died after Georg Cantor."
    COMBINATION LOGIC:AND

# The complex claim is that Barton Mine was halted by a natural disaster not Camlaren Mine.
def simple claims():
    halted(Barton Mine,natural disaster):"Barton Mine was halted by a natural disaster."
    not halted(Camlaren Mine,natural disaster):"Camlaren Mine was not halted by a natural disaster."
    COMBINATION LOGIC:AND
    
# The complex claim is that French people are referring to African ancestry or Afro-Caribbean when they use the term banlieues.
def simple claims():
    refer(French people,African ancestry):"French people are referring to African ancestry when they use the term banlieues."
    refer(French people,Afro-Caribbean):"French people are referring to Afro-Caribbean when they use the term banlieues."
    COMBINATION LOGIC:OR
        
# The complex claim is that Bitter Jester and The Future of Food are not both documentaries about food.
def simple claims():
    documentaries about food(Bitter Jester):"Bitter Jester is documentaries about food."
    documentaries about food(The Future of Food):"The Future of Food is documentaries about food."
    COMBINATION LOGIC:NAND

# The complex claim is that [[CLAIM]]
def simple claims():'''

HOVER_QUESTION = ''''Detect if there are indirect or insufficient mentions in simple claims. 
If so, make questions to query indirect or insufficient mentions, and then use {answer} label to mask the corresponding mention in following text, and the final result will include answer=Question() pairs and claims_to_verify of rest claims.
If not, don't make any questions, and the final result will only have claims_to_verify.
Here are some examples with tips to learn, and you only give the result for last group of simple claims.

# The simple claims are
    "M.I.L.F.$ was recorded by Fergie."
    "M.I.L.F.$ was produced by Polow da Don."
    "M.I.L.F.$ was followed by Life Goes On."
def result():
    claims_to_verify = ["M.I.L.F.$ was recorded by Fergie.","M.I.L.F.$ was produced by Polow da Don.","M.I.L.F.$ was followed by Life Goes On."]

# The simple claims are
    "Before I Go to Sleep stars an Australian actress.",
    "The Australian actress is a producer and occasional singer."
def result():
    answer_1 = Question("Who is the Australian actress stars in Before I Go to Sleep?")
    claims_to_verify = ["{answer_1} is also a producer and occasional singer."]

# The simple claims are
    "Howard University Hospital is located in Washington, D.C."
    "Providence Hospital is located in Washington, D.C."
def result():
    claims_to_verify = ["Howard University Hospital is located in Washington, D.C.","Providence Hospital is located in Washington, D.C."]
    
# The simple claims are
    "The WWE Super Tuesday took place at an arena."
    "That arena currently goes by the name TD Garden."
def result():
    answer_1 = Question("Which arena the WWE Super Tuesday took place?")
    claims_to_verify = ["{answer_1} currently goes by the name TD Garden."]
    
# The simple claims are
    "Carnegie Hall Tower is located in the same city as Staten Island."
def result():
    answer_1 = Question("In which city is Staten Island located?")
    claims_to_verify = ["Carnegie Hall Tower is located in the {answer_1}."]

# The simple claims are
    "Stephanie Caroline March is an American actress."
    "Stephanie Caroline March stars in the movie 'Innocence'."
    "Stephanie Caroline March is best known for Stephanie Caroline March role as Alexandra Cabot in a long-running NBC series."
def result():
    claims_to_verify = ["Stephanie Caroline March is an American actress.","Stephanie Caroline March stars in the movie 'Innocence'.","Stephanie Caroline March is best known for Stephanie Caroline March role as Alexandra Cabot in a long-running NBC series."]
    
# The simple claims are
    "Gina Bramhill was born in a village."
    "The 2011 population of the area that includes this village was 167,446."
def result():
    answer_1 = Question("Which village was Gina Bramhill born in?")
    claims_to_verify = ["The 2011 population of the area that includes {answer_1} was 167,446."]
    
# The simple claims are
    "Sian Gibson co-wrote the British sitcom the British sitcom Peter Kay's Car Share."
    "the British sitcom Peter Kay's Car Share is set around a supermarket and car share scheme."
def result():
    claims_to_verify = ["Sian Gibson co-wrote the British sitcom the British sitcom Peter Kay's Car Share.","the British sitcom Peter Kay's Car Share is set around a supermarket and car share scheme."]
    
# The simple claims are
    "Martin O'Neill replaced the manager."
    "The manager began at Aston Villa Football Club."
def result():
    answer_1 = Question("Who is the manager replaced by Martin O'Neill?")
    claims_to_verify = ["{answer_1} began at Aston Villa Football Club."]

# The simple claims are
    "The Irish film was directed by Paddy Breathnach.",
    "The star of the Irish film played Marcus Agrippa in the HBO drama series 'Rome'."
def result():
    answer_1 = Question("What Irish film did Stanley Kubrick direct?")
    answer_2 = Question("Who is the star of {answer_1}?")
    claims_to_verify = ["{answer_2} played Marcus Agrippa in the HBO drama series \"Rome\".]
    
# The simple claims are
    "Nell Gwyn was the long-time mistress of King Charles II of England."
    "Nell Gwyn occupied a townhouse in Pall Mall, London."
def result():
    claims_to_verify = ["Nell Gwyn was the long-time mistress of King Charles II of England.","Nell Gwyn occupied a townhouse in Pall Mall, London."]
    
# The simple claims are
    "The French singer-songwriter, musician, actress and model was born on 22 December 1972."
    "The live album of The French singer-songwriter, musician, actress and model is Divinidylle Tour."
def result():
    answer_1 = Question("Who is the French singer-songwriter, musician, actress and model that was born on 22 December 1972?")
    claims_to_verify = ["The live album of {answer_1} is Divinidylle Tour."]
    
# The simple claims are
    "The historical Nimavar school is located in the Nimavar Bazaar."
    "The Nimavar Bazaar is located in Iran."
def result():
    claims_to_verify = ["The historical Nimavar school is located in the Nimavar Bazaar.","The Nimavar Bazaar is located in Iran."]

# The simple claims are
    "Thomas Loren Friedman has won more Pulitzer Prizes than Colson Whitehead."
def result():
    answer_1 = Question("How many Pulitzer Prizes has Colson Whitehead won?")
    claims_to_verify = ["Thomas Loren Friedman has won Pulitzer Prizes more than {answer_1}."]
    
# The simple claims are
    "SkyHigh Mount Dandenong is a restaurant located on top of Mount Dandenong, Victoria, Australia."
    "SkyHigh Mount Dandenong is formerly known as Mount Dandenong Observatory."
def result():
    claims_to_verify = ["SkyHigh Mount Dandenong is a restaurant located on top of Mount Dandenong, Victoria, Australia.","SkyHigh Mount Dandenong is formerly known as Mount Dandenong Observatory."]

# The simple claims are
    "Vladimir Igorevich Arnold died after Georg Cantor."
def result():
    answer_1 = Question("When did Georg Cantor die?")
    claims_to_verify = ["Vladimir Igorevich Arnold died after {answer_1}."]
    
# The simple claims are
    "Eatza Pizza and Your Pie were not founded in the same state."
def result():
    answer_1 = Question("Where was Your Pie founded in?")
    claims_to_verify = ["Eatza Pizza is not founded in {answer_1}."]

# The simple claims are
    "Fred Mace played for the Stalybridge Celtic Football Club."
    "the Stalybridge Celtic Football Club is an English football club."
    "Fred Mace played for the Stalybridge Celtic Football Club in 1919."
def result():
    claims_to_verify = ["Fred Mace played for the Stalybridge Celtic Football Club.","the Stalybridge Celtic Football Club is an English football club.","Fred Mace played for the Stalybridge Celtic Football Club in 1919."]

# The simple claims are
    "Stephen King wrote the novel."
    "The movie directed by Stanley Kubrick was based on the novel."
    "The movie directed by Stanley Kubrick was sampled in the album 'Where Blood and Fire Bring Rest'." 
def result():
    answer_1 = Question("What is the movie directed by Stanley Kubrick and  sampled in the album \"Where Blood and Fire Bring Rest\"?")
    answer_2 = Question("What novel is {answer_1} based on?")
    claims_to_verify = ["Stephen King wrote {answer_2}."]

# The simple claims are [[D_CLAIM]]
def result():'''

class Prompt_Loader:
    def __init__(self) -> None:
        self.hover_1 = HOVER_CLAIM
        self.hover_2 = HOVER_QUESTION

    def prompt_construction(self, claim, dataset_name):
        template = None
        if dataset_name == 'HOVER':
            template = self.hover_1
        else:
            raise NotImplementedError
        return template.replace('[[CLAIM]]', claim)

    def prompt_construction_a(self, d_claim, dataset_name):
        d_claim = '"' + d_claim.strip() + '"'
        d_claim = d_claim.replace('\n', '"   "')
        template = None
        if dataset_name == 'HOVER':
            template = self.hover_2
        else:
            raise NotImplementedError
        return template.replace('[[D_CLAIM]]', d_claim)
