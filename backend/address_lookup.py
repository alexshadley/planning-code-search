from typing import List, TypedDict
import pandas as pd
import geopandas as gpd
from shapely import wkt
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
import dotenv

dotenv.load_dotenv()


def load_geo_from_csv(file_name, geo_col):
    df = pd.read_csv(file_name)
    df[geo_col] = df[geo_col].apply(wkt.loads)
    df = gpd.GeoDataFrame(df, geometry=geo_col)

    return df


prc = load_geo_from_csv("./sf_parcels.csv.gz", "shape")
zn = load_geo_from_csv("./sf_zoning.csv.gz", "the_geom")


model = ChatOpenAI(model="gpt-3.5-turbo-1106")


class Address(BaseModel):
    number: int = Field(description="the house number of the address")
    street: str = Field(
        description="the street the address is on, in all caps, without any suffix like st or rd"
    )


class AddressResponse(BaseModel):
    addresses: List[Address] = Field(description="all addresses found in the query")


def extract_addresses(query: str) -> List[Address]:
    template_str = """
    Extract addresses from the following query.

    {query}

    {format_instructions}
    """

    parser = PydanticOutputParser(pydantic_object=AddressResponse)
    prompt = PromptTemplate(
        template=template_str,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    prompt_and_model = prompt | model
    output = prompt_and_model.invoke(
        {
            "query": query,
        }
    )
    response = parser.invoke(output)

    return [a for a in response.addresses if str(a.number) in query]


def get_data_for_addresses(addresses: List[Address]):
    result = []
    for a in addresses:
        parcels = prc[
            (prc["street_name"] == a.street)
            & (prc["from_address_num"] <= a.number)
            & (a.number <= prc["to_address_num"])
        ]
        zoning = gpd.sjoin(parcels, zn, how="inner", predicate="intersects")

        result.append(
            {
                "address": a,
                "zoning_use_district": zoning["zoning"].tolist(),
                "zoning_use_district_name": zoning["districtname"].tolist(),
            }
        )

    return result
